from rest_framework.pagination import CursorPagination

class CartPagination(CursorPagination):
    page_size = 12

    ordering = (
        "-created_at",
        "-id",
    )