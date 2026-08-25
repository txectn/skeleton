from django.contrib import admin

from unfold.admin import ModelAdmin

from .models import ProductMetrics

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