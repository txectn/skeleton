from django.contrib import admin
from django.db.models import Count

from unfold.admin import ModelAdmin

from ..models import Model

@admin.register(Model)
class ModelAdmin(ModelAdmin):
    list_display = (
        "name",
        "brand",
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
        "brand__name",
    )

    list_filter = (
        "brand",
        "created_at",
    )

    autocomplete_fields = (
        "brand",
    )

    prepopulated_fields = {
        "slug": ("name",),
    }

    readonly_fields = (
        "created_at",
    )

    ordering = (
        "brand__name",
        "name",
    )

    list_per_page = 50

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        return queryset.select_related("brand").annotate(
            _product_count=Count("products", distinct=True)
        )

    @admin.display(
        description="Products",
        ordering="_product_count",
    )
    def product_count(self, obj):
        return obj._product_count