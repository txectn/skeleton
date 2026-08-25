from django.db.models import QuerySet

from .base import BaseSort

class MostSoldSort(BaseSort):
    """
    Sorts products by total sale count, highest first.
    """

    SORT_KEY = "most_sold"

    def apply(self, queryset: QuerySet) -> QuerySet:
        return queryset.order_by(
            "-metrics__sold_count",
            "-id",
        )