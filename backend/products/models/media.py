from django.db import models

from .product import Product

class Media(models.Model):
    class MediaType(models.TextChoices):
        IMAGE = "image", "Image"
        VIDEO = "video", "Video"

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="media",
    )

    file = models.FileField(
        upload_to="products/media/",
    )

    media_type = models.CharField(
        max_length=20,
        choices=MediaType.choices,
    )

    alt_text = models.CharField(
        max_length=255,
        blank=True,
    )

    position = models.PositiveIntegerField(
        default=0,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        db_table = "product_media"
        ordering = ["position", "id"]
        constraints = [
            models.UniqueConstraint(
                fields=["product", "position"],
                name="unique_product_media_position",
            ),
        ]
        indexes = [
            models.Index(
                fields=["product", "position"],
                name="media_product_position_idx",
            ),
            models.Index(
                fields=["product", "media_type"],
                name="media_product_type_idx",
            ),
        ]

    def __str__(self):
        return f"{self.product.name} - {self.media_type}"