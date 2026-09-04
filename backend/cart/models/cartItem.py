from django.db import models

from products.models import Variant

from .cart import Cart

class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items",
    )

    variant = models.ForeignKey(
        Variant,
        on_delete=models.CASCADE,
        related_name="cart_items",
    )

    quantity = models.PositiveIntegerField(
        default=1,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["cart", "variant"],
                name="unique_cart_variant",
            ),
        ]

    def __str__(self):
        return f"{self.variant} × {self.quantity}"