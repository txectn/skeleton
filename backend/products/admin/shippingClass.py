from django.contrib import admin

from unfold.admin import ModelAdmin

from ..models import ShippingClass

@admin.register(ShippingClass)
class ShippingClassAdmin(ModelAdmin):
    list_display = (
        "name",
        "delivery_charge",
    )

    list_display_links = (
        "name",
    )

    search_fields = (
        "name",
    )

    ordering = (
        "name",
    )

    list_per_page = 50