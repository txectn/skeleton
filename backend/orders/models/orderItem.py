from django.db import models

from .order import Order

class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
    )

    variant = models.ForeignKey(
        "products.Variant",
        on_delete=models.PROTECT,
        related_name="order_items",
    )

    quantity = models.PositiveIntegerField()

    unit_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    discount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )