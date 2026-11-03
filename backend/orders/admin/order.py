from django import forms
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.contrib import admin
from django.db.models import Exists, OuterRef
from django.utils.html import format_html
from django.urls import NoReverseMatch, reverse

from unfold.admin import ModelAdmin, TabularInline, StackedInline

from ..models import Order, OrderItem
from ..services import (
    process_order_fulfillment,
    process_order_cancellation,
    process_order_failure,
)
from payments.models import Payment, PaymentAttempt
from returns.models import ReturnRequest

from metrics.tasks import update_analytical_metrics

class HasReturnRequestFilter(admin.SimpleListFilter):
    title = "Return Request"
    parameter_name = "has_return_request"

    def lookups(self, request, model_admin):
        return (
            ("yes", "Has Return Request"),
            ("no", "No Return Request"),
        )

    def queryset(self, request, queryset):
        value = self.value()

        if value not in ("yes", "no"):
            return queryset

        queryset = queryset.annotate(
            has_return_request=Exists(
                ReturnRequest.objects.filter(order_id=OuterRef("pk"))
            )
        )

        return queryset.filter(has_return_request=(value == "yes"))


class OrderAdminForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()

        new_status = cleaned_data.get("status")
        old_status = self.initial.get("status")

        if (
            self.instance.pk
            and new_status != old_status
            and self.instance.return_requests.exclude(
                status__in=[
                    ReturnRequest.Status.COMPLETED,
                    ReturnRequest.Status.FAILED,
                    ReturnRequest.Status.CANCELLED,
                ]
            ).exists()
        ):
            self.add_error(
                "status",
                "This order has a return request. "
                "Manage it through the return workflow.",
            )

        return cleaned_data

    class Meta:
        model = Order
        fields = "__all__"


class ReturnRequestInline(TabularInline):
    model = ReturnRequest
    extra = 0


class PaymentAttemptInline(TabularInline):
    model = PaymentAttempt
    extra = 0


class PaymentInline(StackedInline):
    model = Payment
    extra = 0


class OrderItemInline(TabularInline):
    model = OrderItem
    extra = 0
    can_delete = False
    show_change_link = False

    fields = (
        "item_link",
        "variant",
        "quantity",
        "unit_price",
        "discount",
        "total",
    )

    readonly_fields = (
        "item_link",
        "variant",
        "quantity",
        "unit_price",
        "discount",
        "total",
    )

    @admin.display(description="Order Item")
    def item_link(self, obj):
        if not obj or not obj.pk:
            return "-"

        try:
            url = reverse(
                "admin:orders_orderitem_change",
                args=[obj.pk],
            )
        except NoReverseMatch:
            return f"Order Item #{obj.pk} (admin page unavailable)"

        return format_html(
            '<a style="color: var(--color-primary-500);" href="{}">'
            "View Order Item {}</a>",
            url,
            obj.pk,
        )


@admin.register(Order)
class OrderAdmin(ModelAdmin):
    form = OrderAdminForm

    list_display = (
        "id",
        "user",
        "status",
        "subtotal",
        "discount",
        "shipping",
        "total",
        "created_at",
    )

    list_display_links = (
        "id",
        "user",
    )

    list_filter = (
        HasReturnRequestFilter,
        "status",
        "created_at",
    )

    search_fields = (
        "=id",
    )

    readonly_fields = (
        "user",
        "subtotal",
        "discount",
        "shipping",
        "shipping_cost",
        "total",
        "shipping_country",
        "shipping_region",
        "shipping_city",
        "shipping_address",
        "phone_number",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Order",
            {
                "fields": (
                    "user",
                    "status",
                ),
            },
        ),
        (
            "Shipping Information",
            {
                "fields": (
                    "shipping_country",
                    "shipping_region",
                    "shipping_city",
                    "shipping_address",
                    "phone_number",
                ),
            },
        ),
        (
            "Order Totals",
            {
                "fields": (
                    "subtotal",
                    "discount",
                    "shipping",
                    "shipping_cost",
                    "total_shipping_price",
                    "total",
                ),
            },
        ),
        (
            "Timestamps",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )

    inlines = (
        OrderItemInline,
        PaymentInline,
        ReturnRequestInline,
    )

    # def save_model(self, request, obj, form, change):
    #     super().save_model(request, obj, form, change)

    #     if obj.status == Order.Status.DELIVERED:
    #         process_order_fulfillment(obj)
    #         update_analytical_metrics.delay(obj.id)

    #     elif obj.payment.status == Payment.Status.PAID:
    #         update_analytical_metrics.delay(obj.id)

    #     elif obj.status == Order.Status.CANCELLED:
    #         process_order_cancellation(obj)

    #     elif obj.status == Order.Status.FAILED:
    #         process_order_failure(obj)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        try:
            if obj.status == Order.Status.DELIVERED:
                process_order_fulfillment(obj)
                update_analytical_metrics.delay(obj.id)

            elif obj.status == Order.Status.CANCELLED:
                process_order_cancellation(obj)

            elif obj.status == Order.Status.FAILED:
                process_order_failure(obj)

            if obj.payment.status == Payment.Status.PAID:
                update_analytical_metrics.delay(obj.id)

        except ValidationError as e:
            self.message_user(
                request,
                f"Order #{obj.id}: {e}",
                level=messages.ERROR
            )