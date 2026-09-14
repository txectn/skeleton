from django.db import models

from .shippingZone import ShippingZone
from .shippingClass import ShippingClass

class ShippingClassRate(models.Model):

    shipping_class = models.ForeignKey(
        ShippingClass,
        on_delete=models.CASCADE,
        related_name="shipping_class_rates",
    )

    shipping_zone = models.ForeignKey(
        ShippingZone,
        on_delete=models.CASCADE,
        related_name="shipping_class_rates",
        blank=True,
        null=True,
    )

    inner_zone_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )

    outer_zone_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )

    flat_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["shipping_class", "shipping_zone"],
                name="unique_shipping_class_zone",
            )
        ]

    def __str__(self):
        if self.shipping_zone:
            return f"{self.shipping_class} - {self.shipping_zone}"

        return f"{self.shipping_class} - Flat"