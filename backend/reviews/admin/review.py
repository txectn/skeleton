from django.contrib import admin
from unfold.admin import ModelAdmin

from ..models import Review

@admin.register(Review)
class ReviewAdmin(ModelAdmin):
    list_display = (
        "id",
        "product",
        "user",
        "rating",
        "title",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "rating",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "title",
        "message",
        "product__name",
        "user__email",
    )

    ordering = (
        "-created_at",
        "-id",
    )

    autocomplete_fields = (
        "user",
        "product",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    list_per_page = 25
    date_hierarchy = "created_at"
    list_select_related = (
        "user",
        "product",
    )

    fieldsets = (
        (
            "Review Information",
            {
                "classes": ("tab",),
                "fields": (
                    "product",
                    "user",
                    "rating",
                    "title",
                    "message",
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