
from django.contrib import admin

from unfold.admin import ModelAdmin

from ..models import InventoryStockLevel

@admin.register(InventoryStockLevel)
class InventoryStockLevelAdmin(ModelAdmin):
    list_display = (
        "id",
        "name",
        "created_at",
    )

    list_display_links = (
        "id",
        "name",
    )

    search_fields = (
        "=id",
        "name",
    )

    readonly_fields = (
        "created_at",
    )

    ordering = (
        "id",
    )

    fieldsets = (
        (
            "General",
            {
                "fields": (
                    "name",
                ),
            },
        ),
        (
            "Stock Level Configuration",
            {
                "fields": (
                    "levels",
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
