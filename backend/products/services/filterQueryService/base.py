from django.db.models import QuerySet

class BaseFilter:
    """
    Base interface for product filters.
    """

    def apply(self, queryset: QuerySet, params):
        raise NotImplementedError