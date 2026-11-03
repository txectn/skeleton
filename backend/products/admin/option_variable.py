from django.contrib import admin

from unfold.admin import ModelAdmin

from ..models import OptionVariable

@admin.register(OptionVariable)
class OptionVariableAdmin(ModelAdmin):
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

    list_filter = (
        "name",
        "created_at",
    )

    readonly_fields = (
        "created_at",
    )

    ordering = (
        "name",
    )