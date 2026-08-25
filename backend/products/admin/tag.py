from django.contrib import admin

from unfold.admin import ModelAdmin

from ..models import Tag

@admin.register(Tag)
class TagAdmin(ModelAdmin):
    list_display = (
        "name",
        "slug",
        "product_count",
    )

    list_display_links = (
        "name",
    )

    search_fields = (
        "name",
        "slug",
    )
    
    prepopulated_fields = {
        "slug": ("name",),
    }

    ordering = (
        "name",
    )

    list_per_page = 50

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        return queryset.prefetch_related("products")

    @admin.display(
        description="Products",
    )
    def product_count(self, obj):
        return obj.products.count()