from django.contrib import admin

from ..models import SynonymGroup, SynonymTerm

@admin.register(SynonymGroup)
class SynonymGroupAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "is_active",
        "term_count",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "is_active",
    )
    search_fields = (
        "name",
    )
    ordering = (
        "name",
    )

    @admin.display(description="Terms")
    def term_count(self, obj):
        return obj.terms.count()

@admin.register(SynonymTerm)
class SynonymTermAdmin(admin.ModelAdmin):
    list_display = (
        "term",
        "group",
        "is_active",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "is_active",
        "group",
    )
    search_fields = (
        "term",
        "group__name",
    )
    ordering = (
        "term",
    )