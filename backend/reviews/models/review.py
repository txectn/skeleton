from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from products.models import Product

class Review(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews",
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="reviews",
    )

    rating = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ],
    )

    title = models.CharField(
        max_length=255,
        blank=True,
    )

    message = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        db_table = "reviews_reviews"
        ordering = ["-created_at", "-id"]

        constraints = [
            models.UniqueConstraint(
                fields=["user", "product"],
                name="reviews_user_product_unique",
            ),
        ]

        indexes = [
            models.Index(
                fields=["product", "-created_at"],
                name="reviews_product_created_idx",
            ),
            models.Index(
                fields=["product", "rating"],
                name="reviews_product_rating_idx",
            ),
        ]

    def __str__(self):
        return f"{self.product} - {self.rating}/5 - {self.user}"