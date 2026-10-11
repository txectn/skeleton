from django.contrib import admin

from .models import ReturnPolicy, ReturnRequest

@admin.register(ReturnPolicy)
class ReturnPolicyAdmin(admin.ModelAdmin):

    list_display = [
        "name",
        "return_window_days",
        "customer_return_charge",
        "allow_changed_mind",
        "allow_ordered_by_mistake",
        "allow_wrong_product",
        "allow_damaged",
        "allow_fake",
        "allow_not_as_described",
        "allow_missing_item",
        "allow_other",
        "is_active",
        "created_at",
        "updated_at",
    ]

    list_filter = [
        "is_active",
        "allow_changed_mind",
        "allow_ordered_by_mistake",
        "allow_wrong_product",
        "allow_damaged",
        "allow_fake",
        "allow_not_as_described",
        "allow_missing_item",
        "allow_other",
    ]

    search_fields = [
        "name",
    ]

@admin.register(ReturnRequest)
class ReturnRequestAdmin(admin.ModelAdmin):

    list_display = [
        "id",
        "order",
        "reason",
        "status",
        "decision",
        "money_refund_status",
        "return_charge",
        "refund_amount",
        "created_at",
        "updated_at",
    ]

    list_filter = [
        "status",
        "decision",
        "money_refund_status",
        "reason",
    ]

    search_fields = [
        "id",
        "order__id",
        "order__user__email",
    ]

    autocomplete_fields = [
        "order",
    ]