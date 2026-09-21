from unfold.admin import ModelAdmin, TabularInline
from django.contrib import admin

from ..models import Order, OrderItem

class OrderItemInline(TabularInline):
    model = OrderItem
    extra = 0
    can_delete = False

    fields = (
        "variant",
        "quantity",
        "unit_price",
        "discount",
        "total",
    )

    readonly_fields = (
        "variant",
        "quantity",
        "unit_price",
        "discount",
        "total",
    )


@admin.register(Order)
class OrderAdmin(ModelAdmin):

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

    list_filter = (
        "status",
        "created_at",
    )

    search_fields = (
        "id",
        "user__email",
        "phone_number",
    )

    readonly_fields = (
        "user",
        "subtotal",
        "discount",
        "shipping",
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
    )