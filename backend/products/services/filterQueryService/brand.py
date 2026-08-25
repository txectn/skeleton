from django.db.models import QuerySet

from .base import BaseFilter

class BrandFilter(BaseFilter):
    """
    Filters products by brand.
    """

    def apply(self, queryset: QuerySet, params):
        brand = params.get("brand")

        if not brand:
            return queryset

        if not brand.isdigit():
            return queryset

        return queryset.filter(
            brand_id=int(brand),
        )