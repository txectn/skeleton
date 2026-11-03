from django.contrib import admin

from unfold.admin import ModelAdmin

from ..models import Inventory, InventoryStockLevel

DEFAULT_STOCK_LEVELS = [
    {
        "name": "Out of stock (0)",
        "min_quantity": 0,
        "max_quantity": 0,
        "position": 1,
    },
    {
        "name": "Low stock (1–5)",
        "min_quantity": 1,
        "max_quantity": 5,
        "position": 2,
    },
    {
        "name": "Medium stock (6–10)",
        "min_quantity": 6,
        "max_quantity": 10,
        "position": 3,
    },
    {
        "name": "High stock (11–20)",
        "min_quantity": 11,
        "max_quantity": 20,
        "position": 4,
    },
    {
        "name": "In stock (21+)",
        "min_quantity": 21,
        "max_quantity": None,
        "position": 5,
    },
]

class InventoryQuantityFilter(admin.SimpleListFilter):
    title = "quantity range"
    parameter_name = "quantity_range"

    def lookups(self, request, model_admin):
        levels = self.get_levels()

        return tuple(
            (
                str(index),
                level["name"],
            )
            for index, level in enumerate(levels)
        )

    def get_levels(self):
        config = InventoryStockLevel.objects.order_by("id").first()

        if config and isinstance(config.levels, list) and config.levels:
            return sorted(
                config.levels,
                key=lambda level: level.get("position", 0),
            )

        return DEFAULT_STOCK_LEVELS

    def queryset(self, request, queryset):
        value = self.value()

        if value is None:
            return queryset

        try:
            index = int(value)
            levels = self.get_levels()
            level = levels[index]
        except (ValueError, IndexError, TypeError):
            return queryset

        min_quantity = level.get("min_quantity")
        max_quantity = level.get("max_quantity")

        filters = {}

        if min_quantity is not None:
            filters["quantity__gte"] = min_quantity

        if max_quantity is not None:
            filters["quantity__lte"] = max_quantity

        return queryset.filter(**filters)


@admin.register(Inventory)
class InventoryAdmin(ModelAdmin):
    list_display = (
        "id",
        "variant",
        "quantity",
        "reserved_quantity",
        "available_quantity",
        "updated_at",
    )

    list_display_links = (
        "id",
        "variant",
    )

    search_fields = (
        "=id",
        "variant__sku",
        "variant__product__name",
    )

    list_filter = (
        InventoryQuantityFilter,
        "updated_at",
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