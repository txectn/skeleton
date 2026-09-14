from django.contrib import admin

from unfold.admin import ModelAdmin

from .models import Promotion, PromotionVariant

@admin.register(Promotion)
class PromotionAdmin(ModelAdmin):
    list_display = (
        "name",
        "discount_type",
        "discount_value",
        "priority",
        "is_active",
        "created_at",
    )

    list_filter = (
        "discount_type",
        "is_active",
    )

    search_fields = (
        "name",
        "description",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "-priority",
        "-created_at",
    )

    fieldsets = (
        (
            "Promotion",
            {
                "fields": (
                    "name",
                    "description",
                    "discount_type",
                    "discount_value",
                    "priority",
                    "is_active",
                ),
            },
        ),
        (
            "Metadata",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )


@admin.register(PromotionVariant)
class PromotionVariantAdmin(ModelAdmin):
    list_display = (
        "promotion",
        "variant",
        "starts_at",
        "ends_at",
        "created_at",
    )

    list_filter = (
        "promotion__discount_type",
        "promotion__is_active",
    )

    search_fields = (
        "promotion__name",
        "variant__sku",
        "variant__product__name",
    )

    autocomplete_fields = (
        "promotion",
        "variant",
    )

    readonly_fields = (
        "created_at",
    )

    ordering = (
        "-created_at",
    )

    fieldsets = (
        (
            "Assignment",
            {
                "fields": (
                    "promotion",
                    "variant",
                ),
            },
        ),
        (
            "Schedule",
            {
                "fields": (
                    "starts_at",
                    "ends_at",
                ),
            },
        ),
        (
            "Metadata",
            {
                "fields": (
                    "created_at",
                ),
            },
        ),
    )
