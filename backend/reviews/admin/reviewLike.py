from django.contrib import admin
from unfold.admin import ModelAdmin

from ..models import ReviewLike

@admin.register(ReviewLike)
class ReviewLikeAdmin(ModelAdmin):
    list_display = (
        "id",
        "review",
        "user",
        "created_at",
    )

    list_filter = (
        "created_at",
    )

    search_fields = (
        "review__title",
        "review__message",
        "user__email",
    )

    ordering = (
        "-created_at",
        "-id",
    )

    autocomplete_fields = (
        "user",
        "review",
    )

    readonly_fields = (
        "created_at",
    )

    list_per_page = 25
    date_hierarchy = "created_at"
    list_select_related = (
        "user",
        "review",
    )

    fieldsets = (
        (
            "Like Information",
            {
                "classes": ("tab",),
                "fields": (
                    "review",
                    "user",
                ),
            },
        ),
        (
            "Timestamps",
            {
                "classes": ("tab",),
                "fields": (
                    "created_at",
                ),
            },
        ),
    )