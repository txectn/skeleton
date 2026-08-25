from django.db import models

from products.models import Product

class ProductMetrics(models.Model):
    """
    Aggregated behavioral and sales metrics for a product.
    """

    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        related_name="metrics",
    )

    # Activity metrics
    view_count = models.PositiveBigIntegerField(default=0)
    cart_add_count = models.PositiveBigIntegerField(default=0)
    wishlist_count = models.PositiveBigIntegerField(default=0)
    sold_count = models.PositiveBigIntegerField(default=0)

    # Derived ranking scores
    trending_score = models.FloatField(default=0.0)
    popularity_score = models.FloatField(default=0.0)

    # Tracking
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Product Metrics"
        verbose_name_plural = "Product Metrics"

    def __str__(self):
        return f"Metrics for {self.product}"