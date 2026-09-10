from django.contrib import admin

from unfold.admin import ModelAdmin

from .models import Offer, OfferVariant

@admin.register(Offer)
class OfferAdmin(ModelAdmin):
    list_display = (
        "name",
        "discount_type",
        "discount_value",
        "priority",
        "starts_at",
        "ends_at",
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
            "Offer",
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
                    "updated_at",
                ),
            },
        ),
    )

@admin.register(OfferVariant)
class OfferVariantAdmin(ModelAdmin):
    list_display = (
        "offer",
        "variant",
        "created_at",
    )

    list_filter = (
        "offer__discount_type",
        "offer__is_active",
    )

    search_fields = (
        "offer__name",
        "variant__sku",
        "variant__product__name",
    )

    autocomplete_fields = (
        "offer",
        "variant",
    )

    readonly_fields = (
        "created_at",
    )

    ordering = (
        "-created_at",
    )