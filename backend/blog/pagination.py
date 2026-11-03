from rest_framework.pagination import CursorPagination

# ==========================================
# Pagination
# ==========================================

class BlogCursorPagination(CursorPagination):
    page_size = 12
    ordering = ("-published_at", "-id")

class BlogCommentCursorPagination(CursorPagination):
    page_size = 12
    ordering = ("-created_at", "-id")
