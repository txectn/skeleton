from django.conf import settings
from django.db import models

from .review import Review

class ReviewLike(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="review_likes",
    )

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="likes",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        db_table = "reviews_review_likes"
        ordering = ["-created_at", "-id"]

        constraints = [
            models.UniqueConstraint(
                fields=["user", "review"],
                name="reviews_user_review_like_unique",
            ),
        ]

        indexes = [
            models.Index(
                fields=["review", "-created_at"],
                name="reviewlike_review_created_idx",
            ),
        ]

    def __str__(self):
        return f"{self.user} liked review {self.review_id}"