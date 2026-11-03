from django.contrib import admin
from unfold.admin import ModelAdmin

from ..models import ProductReviewSummary

@admin.register(ProductReviewSummary)
class ProductReviewSummaryAdmin(ModelAdmin):
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

    list_per_page = 25
    date_hierarchy = "updated_at"
    list_select_related = ("product",)

    fieldsets = (
        (
            "Product Information",
            {
                "classes": ("tab",),
                "fields": (
                    "product",
                ),
            },
        ),
        (
            "Review Statistics",
            {
                "classes": ("tab",),
                "fields": (
                    "review_count",
                    "average_rating",
                ),
            },
        ),
        (
            "Rating Distribution",
            {
                "classes": ("tab",),
                "fields": (
                    "rating_1_count",
                    "rating_2_count",
                    "rating_3_count",
                    "rating_4_count",
                    "rating_5_count",
                ),
            },
        ),
        (
            "Timestamps",
            {
                "classes": ("tab",),
                "fields": (
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False