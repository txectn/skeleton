from django.contrib import admin

from unfold.admin import ModelAdmin

from ..models import Brand

@admin.register(Brand)
class BrandAdmin(ModelAdmin):

    list_display = (
        "name",
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
    )

    ordering = (
        "name",
    )

    list_per_page = 50

    list_filter = (
        "created_at",
    )

    prepopulated_fields = {
        "slug": ("name",),
    }

    readonly_fields = (
        "created_at",
    )

    def product_count(self, obj):
        return obj.products.count()

    product_count.short_description = "Products"