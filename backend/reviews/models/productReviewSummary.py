from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from products.models.product import Product

class ProductReviewSummary(models.Model):
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        related_name="review_summary",
    )

    review_count = models.PositiveIntegerField(
        default=0,
    )

    average_rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5),
        ],
    )

    rating_1_count = models.PositiveIntegerField(
        default=0,
    )

    rating_2_count = models.PositiveIntegerField(
        default=0,
    )

    rating_3_count = models.PositiveIntegerField(
        default=0,
    )

    rating_4_count = models.PositiveIntegerField(
        default=0,
    )

    rating_5_count = models.PositiveIntegerField(
        default=0,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        db_table = "reviews_product_review_summaries"

    def __str__(self):
        return f"{self.product} - {self.average_rating}/5 ({self.review_count} reviews)"