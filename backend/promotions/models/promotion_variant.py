from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models

from products.models import Variant

class PromotionVariant(models.Model):
    promotion = models.ForeignKey(
        "promotions.Promotion",
        on_delete=models.CASCADE,
        related_name="promotion_variants",
    )

    variant = models.ForeignKey(
        Variant,
        on_delete=models.CASCADE,
        related_name="promotion_variants",
    )

    starts_at = models.DateTimeField()

    ends_at = models.DateTimeField()

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def clean(self):
        super().clean()

        if self.ends_at <= self.starts_at:
            raise ValidationError({
                "ends_at": "End time must be later than start time."
            })

    def __str__(self):
        return f"{self.promotion} - {self.variant}"

