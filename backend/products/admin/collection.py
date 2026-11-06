from django.contrib import admin
from django.db.models import Count

from django.utils.html import format_html

from unfold.admin import ModelAdmin, TabularInline

from ..models import Product, Collection

# =====================================
# Collection Products Inline
# =====================================

class CollectionProductInline(TabularInline):

    model = Product.collections.through

    extra = 0
    show_change_link = True
    tab = True

    verbose_name = "Product"
    verbose_name_plural = "Collection Products"

# =====================================
# Collection Admin
# =====================================

@admin.register(Collection)
class CollectionAdmin(ModelAdmin):

    list_display = (
        "thumbnail_image",
        "id",
        "collection_info",
        "slug",
        "product_count",
        "created_at",
    )

    list_display_links = (
        "thumbnail_image",
        "id",
        "collection_info",
    )

    search_fields = (
        "=id",
        "name",
        "=slug",
        "description",
    )

    list_filter = (
        "created_at",
    )

    prepopulated_fields = {
        "slug": ("name",),
    }

    fields = (
        "name",
        "slug",
        "description",
        "thumbnail",
        "created_at",
    )

    readonly_fields = (
        "created_at",
    )

    inlines = (
        CollectionProductInline,
    )

    ordering = (
        "name",
    )

    list_per_page = 50

    # =====================================
    # Queryset
    # =====================================

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        return queryset.annotate(
            _product_count=Count("products", distinct=True)
        )

    # =====================================
    # Collection Information
    # =====================================

    @admin.display(
        description="Collection",
        ordering="name",
    )
    def collection_info(self, obj):
        return obj.name

    # =====================================
    # Product Count
    # =====================================

    @admin.display(
        description="Products",
        ordering="_product_count",
    )
    def product_count(self, obj):
        return obj._product_count

    @admin.display(description="Thumbnail")
    def thumbnail_image(self, obj):
        if not obj.thumbnail:
            return "NO IMAGE"

        return format_html(
            '<img src="{}" style="width:40px; height:40px; '
            'object-fit:cover; border-radius:5px;" />',
            obj.thumbnail.url,
        )