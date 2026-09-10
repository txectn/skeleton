# Cursor Pagination Example

from rest_framework.pagination import CursorPagination

class Pagination(CursorPagination):
    page_size = 12

    ordering = (
        "-created_at",
        "-id",
    )

'''
# Page Pagination Example
from rest_framework.pagination import PageNumberPagination

class Pagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = "page_size"
    max_page_size = 100
'''

