from django.contrib import admin

from unfold.admin import ModelAdmin

from ..models import Inventory

@admin.register(Inventory)
class InventoryAdmin(ModelAdmin):
    list_display = (
        "variant",
        "quantity",
        "reserved_quantity",
        "available_quantity",
        "updated_at",
    )

    search_fields = (
        "variant__sku",
        "variant__product__name",
    )

    autocomplete_fields = (
        "variant",
    )

    readonly_fields = (
        "available_quantity",
        "updated_at",
    )

    ordering = (
        "-updated_at",
    )

    @admin.display(
        description="Available",
        ordering="quantity",
    )
    def available_quantity(self, obj):
        return obj.available_quantity