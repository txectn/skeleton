from celery import shared_task

from .services import (
    AnalyticalMetricsService,
)

from .models import AnalyticalMetrics

from products.models import Product

@shared_task
def update_analytical_metrics(order_id):
    AnalyticalMetricsService.update_order_metrics(order_id)

@shared_task
def record_total_products():
    total_products = Product.objects.count()

    AnalyticalMetrics.objects.update_or_create(
        pk=1,
        defaults={
            "total_products": total_products,
        }
    )

@shared_task
def create_metrics_snapshot():
    AnalyticalMetricsService.create_snapshot()