from django.db import models

from products.models import Product

class ProductMetricsSnapshot(models.Model):
    """
    Historical snapshot of a product's aggregated metrics.

    Stores the metric values at a specific point in time so that
    historical activity, growth, trending, and other derived
    metrics can be calculated later.
    """

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="metrics_snapshots",
    )

    # Activity metrics
    view_count = models.PositiveBigIntegerField(default=0)
    cart_add_count = models.PositiveBigIntegerField(default=0)
    wishlist_count = models.PositiveBigIntegerField(default=0)
    sold_count = models.PositiveBigIntegerField(default=0)

    # Snapshot timestamp
    recorded_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        verbose_name = "Product Metrics Snapshot"
        verbose_name_plural = "Product Metrics Snapshots"
        ordering = ["-recorded_at"]
        indexes = [
            models.Index(
                fields=["product", "-recorded_at"],
                name="metrics_snap_prod_time_idx",
            ),
        ]

    def __str__(self):
        return f"Snapshot for {self.product} at {self.recorded_at}"