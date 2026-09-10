from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models

from products.models import Variant

class OfferVariant(models.Model):
    offer = models.ForeignKey(
        "offers.Offer",
        on_delete=models.CASCADE,
        related_name="offer_variants",
    )

    variant = models.ForeignKey(
        Variant,
        on_delete=models.CASCADE,
        related_name="offer_variants",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["offer", "variant"],
                name="unique_offer_variant",
            ),
        ]

    def clean(self):
        super().clean()

        if not self.offer_id or not self.variant_id:
            return

        price = self.variant.price
        cost_price = self.variant.cost_price

        if price is None or cost_price is None:
            return

        discount_value = self.offer.discount_value

        if self.offer.discount_type == self.offer.DiscountType.PERCENTAGE:
            offer_price = price - (
                price * discount_value / Decimal("100")
            )
        else:
            offer_price = price - discount_value

        if offer_price < cost_price:
            raise ValidationError({
                "offer": (
                    f"This offer would reduce the variant price to "
                    f"{offer_price}, which is below the cost price "
                    f"of {cost_price}."
                )
            })

    def __str__(self):
        return f"{self.offer} - {self.variant}"