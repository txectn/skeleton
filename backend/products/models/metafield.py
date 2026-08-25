from django.db import models

from .product import Product

class Metafield(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="metafields",
    )

    namespace = models.CharField(
        max_length=100,
    )

    key = models.CharField(
        max_length=100,
    )

    value = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        db_table = "product_metafields"
        ordering = ["namespace", "key"]
        constraints = [
            models.UniqueConstraint(
                fields=["product", "namespace", "key"],
                name="unique_product_metafield",
            ),
        ]
        indexes = [
            models.Index(
                fields=["product", "namespace"],
                name="meta_product_ns_idx",
            ),
        ]

    def __str__(self):
        return f"{self.namespace}.{self.key}"