from django.contrib import admin

from ..models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
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