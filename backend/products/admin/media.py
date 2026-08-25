from django.contrib import admin

from unfold.admin import ModelAdmin

from ..models import Media

@admin.register(Media)
class MediaAdmin(ModelAdmin):
    list_display = (
        "product",
        "media_type",
        "position",
        "alt_text",
        "created_at",
    )

    list_display_links = (
        "product",
    )

    search_fields = (
        "product__name",
        "alt_text",
    )

    list_filter = (
        "media_type",
        "created_at",
    )

    autocomplete_fields = (
        "product",
    )

    readonly_fields = (
        "created_at",
    )

    ordering = (
        "product",
        "position",
    )

    list_per_page = 50