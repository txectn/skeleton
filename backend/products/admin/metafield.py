from django.contrib import admin

from unfold.admin import ModelAdmin

from ..models import Metafield

@admin.register(Metafield)
class MetafieldAdmin(ModelAdmin):
    list_display = (
        "id",
        "product",
        "namespace",
        "key",
        "value_preview",
        "created_at",
    )

    list_display_links = (
        "id",
        "key",
    )

    search_fields = (
        "=id",
        "product__name",
        "namespace",
        "key",
        "value",
    )

    list_filter = (
        "namespace",
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
        "namespace",
        "key",
    )

    list_per_page = 50

    @admin.display(
        description="Value",
    )
    def value_preview(self, obj):
        if len(obj.value) > 80:
            return f"{obj.value[:80]}..."
        return obj.value