from django.db import transaction
from rest_framework.exceptions import ValidationError

from ..models import CartItem

class CartItemDecreaseService:

    @staticmethod
    @transaction.atomic
    def decrease_quantity(
        *,
        cart,
        variant,
        quantity,
    ):
        """
        Decrease the quantity of an existing CartItem.

        Rules:
            1. The CartItem must already exist.
            2. Quantity must be greater than zero.
            3. Decrease by the requested quantity.
            4. The CartItem quantity must never go below 1.
            5. If the requested decrease exceeds the current
               quantity, set the quantity to 1.
            6. The CartItem is never deleted.

        Returns:
            tuple:
                (
                    cart_item,
                    decrease_limit_reached,
                )
        """

        # ---------------------------------------------------------
        # Validate requested quantity
        # ---------------------------------------------------------

        if quantity <= 0:
            raise ValidationError(
                {
                    "quantity": (
                        "Quantity must be greater than zero."
                    )
                }
            )

        # ---------------------------------------------------------
        # Find CartItem
        # ---------------------------------------------------------

        cart_item = CartItem.objects.filter(
            cart=cart,
            variant=variant,
        ).first()

        # ---------------------------------------------------------
        # CartItem does not exist
        # ---------------------------------------------------------

        if cart_item is None:
            raise ValidationError(
                {
                    "variant": (
                        "This item does not exist in the cart."
                    )
                }
            )

        # ---------------------------------------------------------
        # Calculate requested quantity
        # ---------------------------------------------------------

        requested_quantity = (
            cart_item.quantity - quantity
        )

        # ---------------------------------------------------------
        # Check decrease limit
        # ---------------------------------------------------------

        decrease_limit_reached = (
            requested_quantity < 1
        )

        # ---------------------------------------------------------
        # Calculate new quantity
        # ---------------------------------------------------------

        new_quantity = max(
            1,
            requested_quantity,
        )

        # ---------------------------------------------------------
        # Update CartItem
        # ---------------------------------------------------------

        cart_item.quantity = new_quantity

        cart_item.save(
            update_fields=[
                "quantity",
                "updated_at",
            ],
        )

        return (
            cart_item,
            decrease_limit_reached,
        )