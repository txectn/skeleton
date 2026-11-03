from django.db import models

from orders.models import Order

class AnalyticalMetrics(models.Model):
    total_products = models.PositiveBigIntegerField(default=0)

    total_sales = models.PositiveBigIntegerField(default=0)

    total_revenue = models.PositiveBigIntegerField(default=0)

    profit = models.PositiveBigIntegerField(default=0)

class AnalyticalMetricsSnapshot(models.Model):

    total_products = models.PositiveBigIntegerField(default=0)

    total_sales = models.PositiveBigIntegerField(default=0)

    total_revenue = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0,
    )

    total_profit = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["-created_at"]),
        ]

    def __str__(self):
        return f"Metrics Snapshot - {self.created_at:%Y-%m-%d %H:%M}"

class OrderMetricsRecord(models.Model):
    order = models.OneToOneField(
        Order,
        on_delete=models.PROTECT,
        related_name="metrics_record",
    )

    is_qualified = models.BooleanField(default=False)

    total_sales = models.PositiveBigIntegerField(default=0)

    total_revenue = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0,
    )

    total_profit = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0,
    )

    processed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        verbose_name = "Order Metrics Record"
        verbose_name_plural = "Order Metrics Records"

    def __str__(self):
        return f"Metrics Record - Order {self.order_id}"