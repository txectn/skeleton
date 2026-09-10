from django.contrib import admin

from unfold.admin import ModelAdmin

from .models import ProductMetrics, ProductMetricsSnapshot

@admin.register(ProductMetrics)
class ProductMetricsAdmin(ModelAdmin):
    list_display = (
        "product",
        "view_count",
        "cart_add_count",
        "wishlist_count",
        "sold_count",
        "trending_score",
        "popularity_score",
        "updated_at",
    )

    search_fields = (
        "product__name",
        "product__product_code",
    )

    list_filter = (
        "updated_at",
    )

    ordering = (
        "-trending_score",
        "-popularity_score",
    )

    readonly_fields = (
        # "product",
        # "view_count",
        # "cart_add_count",
        # "wishlist_count",
        # "sold_count",
        # "trending_score",
        # "popularity_score",
        "updated_at",
    )

    autocomplete_fields = (
        "product",
    )



@admin.register(ProductMetricsSnapshot)
class ProductMetricsSnapshotAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "view_count",
        "cart_add_count",
        "wishlist_count",
        "sold_count",
        "recorded_at",
    )

    list_filter = (
        "recorded_at",
    )

    search_fields = (
        "product__name",
        "product__id",
    )

    ordering = (
        "-recorded_at",
    )

    readonly_fields = (
        "product",
        "view_count",
        "cart_add_count",
        "wishlist_count",
        "sold_count",
        "recorded_at",
    )

    list_select_related = (
        "product",
    )

    date_hierarchy = "recorded_at"

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False