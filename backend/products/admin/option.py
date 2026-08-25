from django.contrib import admin

from unfold.admin import ModelAdmin

from ..models import Option

@admin.register(Option)
class OptionAdmin(ModelAdmin):
    list_display = (
        "option_variable",
        "value",
        "product",
        "position",
        "created_at",
    )

    list_filter = (
        "option_variable",
        "product",
    )

    search_fields = (
        "value",
        "product__name",
        "option_variable__name",
    )

    autocomplete_fields = (
        "product",
        "option_variable",
    )

    readonly_fields = (
        "created_at",
    )

    ordering = (
        "product",
        "position",
        "id",
    )