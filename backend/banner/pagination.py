from rest_framework.pagination import CursorPagination

# ==========================================
# Pagination
# ==========================================

class BannerPagination(CursorPagination):
    page_size = 12
    ordering = ("-created_at", "-id")
