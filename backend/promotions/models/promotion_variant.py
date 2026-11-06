from datetime import timedelta

from django.utils import timezone

from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models

from products.models import Variant

from .promotion import Promotion

def default_promotion_end():
    return timezone.now() + timedelta(days=7)


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

    starts_at = models.DateTimeField(
        default=timezone.now,
    )

    ends_at = models.DateTimeField(
        default=default_promotion_end,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def clean(self):
        super().clean()

        if self.ends_at <= self.starts_at:
            raise ValidationError({
                "ends_at": "End time must be later than start time."
            })

        cost_price = Decimal(self.variant.cost_price)
        price = Decimal(self.variant.price)
        discount_value = Decimal(self.promotion.discount_value)

        if self.promotion.discount_type == Promotion.DiscountType.PERCENTAGE:
            discount_amount = (price * discount_value) / Decimal("100")

        elif self.promotion.discount_type == Promotion.DiscountType.FIXED:
            discount_amount = discount_value

        final_price = price - discount_amount

        if final_price <= cost_price:
            raise ValidationError({
                "promotion": "Final price must be greater than cost price."
            })
        
    def __str__(self):
        return f"{self.promotion} - {self.variant}"

