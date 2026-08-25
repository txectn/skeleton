from django.db.models import QuerySet

from .brand import BrandFilter
from .category import CategoryFilter
from .price import PriceFilter
from .inStock import InStockFilter

class ProductFilterService:
    """
    Orchestrates the product filtering pipeline.
    """

    FILTERS = (
        BrandFilter,
        CategoryFilter,
        PriceFilter,
        InStockFilter,
    )

    def __init__(self, filters=None):
        self.filters = filters if filters is not None else self.FILTERS

    def filter(self, queryset: QuerySet, params):
        """
        Apply all configured filters sequentially.
        """
        for filter_class in self.filters:
            queryset = filter_class().apply(
                queryset=queryset,
                params=params,
            )

        return queryset

