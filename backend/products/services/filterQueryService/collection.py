from django.db.models import QuerySet

from .base import BaseFilter

class CollectionFilter(BaseFilter):
    """
    Filters products by collection.
    """

    def apply(self, queryset: QuerySet, params):
        collection = params.get("collection")

        if not collection:
            return queryset

        if not collection.isdigit():
            return queryset

        return queryset.filter(
            collections__id=int(collection),
        )