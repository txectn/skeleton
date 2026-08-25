from django.contrib import admin

from unfold.admin import ModelAdmin

from ..models import Collection

@admin.register(Collection)
class CollectionAdmin(ModelAdmin):
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

    list_filter = (
        "created_at",
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

        return queryset.prefetch_related("products")

    @admin.display(
        description="Products",
    )
    def product_count(self, obj):
        return obj.products.count()