from django.contrib import admin

from unfold.admin import ModelAdmin, TabularInline

from ..models import SynonymGroup, SynonymTerm

class SynonymTermInline(TabularInline):
    model = SynonymTerm
    extra = 0

@admin.register(SynonymGroup)
class SynonymGroupAdmin(ModelAdmin):
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

    inlines = (
        SynonymTermInline,
    )

    ordering = (
        "name",
    )

    list_per_page = 25

    @admin.display(description="Terms", ordering="terms__count")
    def term_count(self, obj):
        return obj.terms.count()

@admin.register(SynonymTerm)
class SynonymTermAdmin(ModelAdmin):
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

    list_per_page = 25

    autocomplete_fields = (
        "group",
    )
