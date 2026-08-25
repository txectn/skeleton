from django.db.models import QuerySet

from .base import BaseSort

class MostViewedSort(BaseSort):
    """
    Sorts products by total view count, highest first.
    """

    SORT_KEY = "most_viewed"

    def apply(self, queryset: QuerySet) -> QuerySet:
        return queryset.order_by(
            "-metrics__view_count",
            "-id",
        )