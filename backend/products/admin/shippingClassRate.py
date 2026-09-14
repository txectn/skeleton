from django.contrib import admin

from unfold.admin import ModelAdmin

from ..models import ShippingClassRate

@admin.register(ShippingClassRate)
class ShippingClassRateAdmin(ModelAdmin):
    list_display = (
        "shipping_class",
        "shipping_zone",
        "inner_zone_rate",
        "outer_zone_rate",
        "flat_rate",
    )

    search_fields = (
        "shipping_class__name",
        "shipping_zone__name",
    )

    ordering = (
        "shipping_class",
        "shipping_zone",
    )

    list_filter = (
        "shipping_class",
        "shipping_zone",
    )

    list_per_page = 50
