from django.db.models import F, QuerySet

from .base import BaseFilter

class InStockFilter(BaseFilter):
    """
    Filters products based on inventory availability.
    """

    PARAM_NAME = "in_stock"

    def apply(self, queryset: QuerySet, params):
        in_stock = params.get(self.PARAM_NAME)

        if in_stock is None:
            return queryset

        if in_stock == "true":
            return queryset.filter(
                variants__inventory__quantity__gt=F(
                    "variants__inventory__reserved_quantity"
                ),
                variants__is_active=True,
            )

        if in_stock == "false":
            return queryset.filter(
                variants__inventory__quantity__lte=F(
                    "variants__inventory__reserved_quantity"
                ),
                variants__is_active=True,
            )

        return queryset