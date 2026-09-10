from django.contrib import admin

from ..models import ReviewLike

@admin.register(ReviewLike)
class ReviewLikeAdmin(admin.ModelAdmin):
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