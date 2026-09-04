from django.db import transaction
from rest_framework.exceptions import ValidationError

from products.models import Inventory

from ..models import CartItem

class CartItemUpdateQuantityService:

    @staticmethod
    @transaction.atomic
    def update_quantity(
        *,
        cart,
        variant,
        quantity,
    ):
        """
        Update the total quantity of an existing CartItem.

        Rules:
            1. The CartItem must already exist.
            2. Quantity must be greater than zero.
            3. Quantity represents the new total quantity.
            4. The quantity must not exceed available inventory.
            5. If the requested quantity exceeds available
               inventory, set it to the maximum available quantity.
            6. The CartItem is never deleted.

        Returns:
            tuple:
                (
                    cart_item,
                    quantity_limit_reached,
                )

        Updating a CartItem does not reserve inventory.
        reserved_quantity is only changed during the
        checkout/order reservation flow.
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
        # Get inventory for the variant
        # ---------------------------------------------------------

        try:
            inventory = variant.inventory

        except Inventory.DoesNotExist:
            raise ValidationError(
                {
                    "variant": (
                        "This variant is not available."
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
        # Get available inventory
        # ---------------------------------------------------------

        available_quantity = inventory.available_quantity

        # ---------------------------------------------------------
        # Check quantity limit
        # ---------------------------------------------------------

        quantity_limit_reached = (
            quantity > available_quantity
        )

        # ---------------------------------------------------------
        # Calculate new quantity
        # ---------------------------------------------------------

        new_quantity = min(
            quantity,
            available_quantity,
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
            quantity_limit_reached,
        )