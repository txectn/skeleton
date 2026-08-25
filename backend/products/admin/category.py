from django.contrib import admin
from django.db.models import Count

from unfold.admin import ModelAdmin

from ..models import Category

@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = (
        "name",
        "parent",
        "slug",
        "product_count",
        "created_at",
    )

    list_display_links = (
        "name",
    )

    search_fields = (
        "name",
        "slug",
        "description",
        "parent__name",
    )

    list_filter = (
        "parent",
        "created_at",
    )

    autocomplete_fields = (
        "parent",
    )

    prepopulated_fields = {
        "slug": ("name",),
    }

    readonly_fields = (
        "created_at",
    )

    ordering = (
        "name",
    )

    list_per_page = 50

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        return queryset.select_related("parent").annotate(
            _product_count=Count("products", distinct=True)
        )

    @admin.display(
        description="Products",
        ordering="_product_count",
    )
    def product_count(self, obj):
        return obj._product_count