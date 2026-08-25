from django.core.exceptions import ValidationError
from django.db import models

class Inventory(models.Model):
    variant = models.OneToOneField(
        "products.Variant",
        on_delete=models.CASCADE,
        related_name="inventory",
    )

    quantity = models.PositiveIntegerField(
        default=0,
    )

    reserved_quantity = models.PositiveIntegerField(
        default=0,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ("-updated_at",)

    def clean(self):
        if self.reserved_quantity > self.quantity:
            raise ValidationError(
                {
                    "reserved_quantity": (
                        "Reserved quantity cannot be greater than total quantity."
                    )
                }
            )

    @property
    def available_quantity(self):
        return self.quantity - self.reserved_quantity

    def __str__(self):
        return f"Inventory — {self.variant.sku}"