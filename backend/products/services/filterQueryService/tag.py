from django.db.models import QuerySet

from .base import BaseFilter

class TagFilter(BaseFilter):
    """
    Filters products by tag.
    """

    def apply(self, queryset: QuerySet, params):
        tag = params.get("tag")

        if not tag:
            return queryset

        if not tag.isdigit():
            return queryset

        return queryset.filter(
            tags__id=int(tag),
        )