from django.db.models import QuerySet

from .mostSold import MostSoldSort
from .mostViewed import MostViewedSort
from .trending import TrendingSort
from .popularity import PopularitySort

class ProductSortService:
    """
    Orchestrates the product sorting pipeline.
    """

    SORTS = (
        MostSoldSort,
        MostViewedSort,
        TrendingSort,
        PopularitySort,
    )

    SORT_PARAM = "sort_by"

    def __init__(self, sorts=None):
        self.sorts = sorts if sorts is not None else self.SORTS

    def sort(
        self,
        queryset: QuerySet,
        params,
    ) -> QuerySet:
        """
        Apply the requested product sorting strategy.
        """
        sort_by = params.get(self.SORT_PARAM)

        if not sort_by:
            return queryset

        for sort_class in self.sorts:
            sort_instance = sort_class()

            if sort_instance.SORT_KEY == sort_by:
                print("SORTING BY:", sort_instance.SORT_KEY)
                return sort_instance.apply(queryset)

        return queryset
