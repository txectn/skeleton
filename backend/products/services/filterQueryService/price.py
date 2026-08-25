from django.db.models import QuerySet

from .base import BaseFilter

class PriceFilter(BaseFilter):
    """
    Filters products by active variant price range.
    """

    MIN_PRICE_PARAM = "min_price"
    MAX_PRICE_PARAM = "max_price"

    def apply(self, queryset: QuerySet, params):
        min_price = params.get(self.MIN_PRICE_PARAM)
        max_price = params.get(self.MAX_PRICE_PARAM)

        if min_price and min_price.isdigit():
            queryset = queryset.filter(
                variants__price__gte=int(min_price),
                variants__is_active=True,
            )

        if max_price and max_price.isdigit():
            queryset = queryset.filter(
                variants__price__lte=int(max_price),
                variants__is_active=True,
            )

        return queryset