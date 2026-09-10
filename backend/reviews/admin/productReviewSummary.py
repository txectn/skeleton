from django.contrib import admin

from ..models import ProductReviewSummary

@admin.register(ProductReviewSummary)
class ProductReviewSummaryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "product",
        "review_count",
        "average_rating",
        "rating_1_count",
        "rating_2_count",
        "rating_3_count",
        "rating_4_count",
        "rating_5_count",
        "updated_at",
    )

    list_filter = (
        "updated_at",
    )

    search_fields = (
        "product__name",
    )

    ordering = (
        "-updated_at",
        "-id",
    )

    autocomplete_fields = (
        "product",
    )

    readonly_fields = (
        "review_count",
        "average_rating",
        "rating_1_count",
        "rating_2_count",
        "rating_3_count",
        "rating_4_count",
        "rating_5_count",
        "created_at",
        "updated_at",
    )