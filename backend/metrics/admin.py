
from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import (
    AnalyticalMetrics,
    AnalyticalMetricsSnapshot,
    OrderMetricsRecord,
)

@admin.register(AnalyticalMetrics)
class AnalyticalMetricsAdmin(ModelAdmin):

    list_display = (
        "id",
        "total_products",
        "total_sales",
        "total_revenue",
        "profit",
    )

    list_display_links = (
        "id",
        "total_products",
        "total_sales",
        "total_revenue",
        "profit",
    )

    readonly_fields = (
        "total_products",
        "total_sales",
        "total_revenue",
        "profit",
    )

    def has_add_permission(self, request):
        return not AnalyticalMetrics.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

@admin.register(AnalyticalMetricsSnapshot)
class AnalyticalMetricsSnapshotAdmin(ModelAdmin):

    list_display = (
        "id",
        "total_products",
        "total_sales",
        "total_revenue",
        "total_profit",
        "created_at",
    )

    list_display_links = (
        "id",
        "total_products",
        "total_sales",
        "total_revenue",
        "total_profit",
        "created_at",
        )

    list_filter = (
        "created_at",
    )

    search_fields = (
        "id",
    )

    readonly_fields = (
        "total_products",
        "total_sales",
        "total_revenue",
        "total_profit",
        "created_at",
    )

    date_hierarchy = "created_at"

    ordering = ("-created_at",)

    list_per_page = 30

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(OrderMetricsRecord)
class OrderMetricsRecordAdmin(ModelAdmin):

    list_display = (
        "id",
        "order",
        "is_qualified",
        "total_sales",
        "total_revenue",
        "total_profit",
        "processed_at",
        "updated_at",
    )

    list_display_links = (
        "id",
        "order",
        "is_qualified",
        "total_sales",
        "total_revenue",
        "total_profit",
        "processed_at",
        "updated_at",
    )

    list_filter = (
        "is_qualified",
        "processed_at",
        "updated_at",
    )

    search_fields = (
        "order__id",
    )

    readonly_fields = (
        "order",
        "is_qualified",
        "total_sales",
        "total_revenue",
        "total_profit",
        "processed_at",
        "updated_at",
    )

    date_hierarchy = "processed_at"

    ordering = ("-updated_at",)

    list_per_page = 30

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
