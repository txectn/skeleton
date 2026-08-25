from django.db.models import QuerySet

from .base import BaseSort

class PopularitySort(BaseSort):
    """
    Sorts products by popularity score, highest first.
    """

    SORT_KEY = "popularity"

    def apply(self, queryset: QuerySet) -> QuerySet:
        return queryset.order_by(
            "-metrics__popularity_score",
            "-id",
        )