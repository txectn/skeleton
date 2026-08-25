from rest_framework.pagination import CursorPagination

from .services.sortQueryService  import ProductSortOrdering

class ProductPagination(CursorPagination):
    """
    Orchestrates cursor pagination ordering for product querysets.
    """

    page_size = 12

    DEFAULT_ORDERING = (
        "-created_at",
        "-id",
    )

    def get_ordering(self, request, queryset, view):
        """
        Determine the ordering used by cursor pagination.

        Priority:
        1. Explicit product sort.
        2. Default product ordering.
        """

        sort_by = request.query_params.get("sort_by")

        if sort_by:
            ordering = ProductSortOrdering.SORT_ORDERINGS.get(sort_by)

            if ordering:
                return ordering

        return self.DEFAULT_ORDERING


'''
# Cursor Pagination Example
from rest_framework.pagination import CursorPagination

class ProductPagination(CursorPagination):
    page_size = 12

    ordering = (
        "-created_at",
        "-id",
    )
'''

'''
# Page Pagination Example
from rest_framework.pagination import PageNumberPagination

class ProductPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = "page_size"
    max_page_size = 100
'''

