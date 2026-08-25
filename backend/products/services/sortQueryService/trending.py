from django.db.models import QuerySet

from .base import BaseSort

class TrendingSort(BaseSort):
    """
    Sorts products by trending score, highest first.
    """

    SORT_KEY = "trending"

    def apply(self, queryset: QuerySet) -> QuerySet:
        return queryset.order_by(
            "-metrics__trending_score",
            "-id",
        )