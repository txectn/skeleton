from django.contrib import admin

from unfold.admin import ModelAdmin

from ..models import ShippingZone

@admin.register(ShippingZone)
class ShippingZoneAdmin(ModelAdmin):
    list_display = (
        "name",
        "country",
        "region",
        "city",
    )

    list_display_links = (
        "name",
    )

    search_fields = (
        "name",
        "country",
        "region",
        "city",
    )

    ordering = (
        "name",
    )

    list_filter = (
        "country",
        "region",
        "city",
    )

    list_per_page = 50
