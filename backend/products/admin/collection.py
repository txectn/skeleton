from django.contrib import admin

from unfold.admin import ModelAdmin

from ..models import Collection

@admin.register(Collection)
class CollectionAdmin(ModelAdmin):
    list_display = (
        "id",
        "name",
        "slug",
        "product_count",
        "created_at",
    )

    list_display_links = (
        "id",
        "name",
    )

    search_fields = (
        "=id",
        "name",
        "=slug",
        "description",
    )

    list_filter = (
        "name",
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