from django.db.models import QuerySet

from .base import BaseFilter

class CategoryFilter(BaseFilter):
    """
    Filters products by category.
    """

    PARAM_NAME = "category"

    def apply(self, queryset: QuerySet, params):
        category_id = params.get(self.PARAM_NAME)

        if not category_id:
            return queryset

        if not category_id.isdigit():
            return queryset

        return queryset.filter(
            category_id=int(category_id),
        )

