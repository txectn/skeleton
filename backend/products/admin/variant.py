from django.contrib import admin

from unfold.admin import ModelAdmin, StackedInline, TabularInline

from ..models import Variant, Inventory

class InventoryInline(TabularInline):
    model = Inventory
    extra = 0

@admin.register(Variant)
class VariantAdmin(ModelAdmin):
    list_display = (
        "sku",
        "product",
        "price",
        "compare_at_price",
        "cost_price",
        "position",
        "is_active",
        "created_at",
    )

    list_filter = (
        "is_active",
        "product",
    )

    search_fields = (
        "sku",
        "product__name",
    )

    autocomplete_fields = (
        "product",
        "options",
        "currency",
    )

    filter_horizontal = (
        "options",
    )

    readonly_fields = (
        "created_at",
    )

    ordering = (
        "product",
        "position",
        "id",
    )

    inlines = (
        InventoryInline,
    )

    @admin.display(
        boolean=True,
        description="Active",
        ordering="is_active",
    )
    def is_active_display(self, obj):
        return obj.is_active