from django.contrib import admin

from unfold.admin import ModelAdmin

from ..models import ReturnPolicy

@admin.register(ReturnPolicy)
class ReturnPolicyAdmin(ModelAdmin):
    list_display = (
        "id",
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
    )

    list_display_links = (
        "id",
        "name",
    )

    list_filter = (
        "is_active",
        "allow_changed_mind",
        "allow_ordered_by_mistake",
        "allow_wrong_product",
        "allow_damaged",
        "allow_fake",
        "allow_not_as_described",
        "allow_missing_item",
        "allow_other",
    )

    search_fields = ("name",)

    ordering = ("-created_at",)

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    list_per_page = 25
    date_hierarchy = "created_at"

    fieldsets = (
        (
            "Policy Information",
            {
                "classes": ("tab",),
                "fields": (
                    "name",
                    "return_window_days",
                    "customer_return_charge",
                    "is_active",
                ),
            },
        ),
        (
            "Allowed Return Reasons",
            {
                "classes": ("tab",),
                "fields": (
                    "allow_changed_mind",
                    "allow_ordered_by_mistake",
                    "allow_wrong_product",
                    "allow_damaged",
                    "allow_fake",
                    "allow_not_as_described",
                    "allow_missing_item",
                    "allow_other",
                ),
            },
        ),
        (
            "Timestamps",
            {
                "classes": ("tab",),
                "fields": (
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )
