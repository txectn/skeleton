from django.db import models

from .brand import Brand

class Model(models.Model):
    brand = models.ForeignKey(
        Brand,
        on_delete=models.PROTECT,
        related_name="models",
    )

    name = models.CharField(
        max_length=255,
    )

    slug = models.SlugField(
        max_length=255,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        db_table = "product_models"
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["brand", "name"],
                name="unique_model_per_brand",
            ),
            models.UniqueConstraint(
                fields=["brand", "slug"],
                name="unique_model_slug_per_brand",
            ),
        ]
        indexes = [
            models.Index(
                fields=["brand", "name"],
                name="model_brand_name_idx",
            ),
            models.Index(
                fields=["brand", "slug"],
                name="model_brand_slug_idx",
            ),
        ]

    def __str__(self):
        return f"{self.brand.name} {self.name}"