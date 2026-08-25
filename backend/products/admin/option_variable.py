from django.contrib import admin

from unfold.admin import ModelAdmin

from ..models import OptionVariable

@admin.register(OptionVariable)
class OptionVariableAdmin(ModelAdmin):
    list_display = (
        "name",
        "created_at",
    )

    search_fields = (
        "name",
    )

    readonly_fields = (
        "created_at",
    )

    ordering = (
        "name",
    )