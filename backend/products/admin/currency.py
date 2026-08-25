from django.contrib import admin

from unfold.admin import ModelAdmin

from ..models import Currency

@admin.register(Currency)
class CurrencyAdmin(ModelAdmin):
    list_display = (
        "code",
        "name",
        "symbol",
    )

    list_display_links = (
        "code",
    )

    search_fields = (
        "code",
        "name",
        "symbol",
    )

    ordering = (
        "code",
    )

    list_per_page = 50