from django.db.models import QuerySet

class BaseSort:
    """
    Base interface for product sorting strategies.
    """

    def apply(self, queryset: QuerySet) -> QuerySet:
        raise NotImplementedError