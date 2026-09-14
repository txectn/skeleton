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
            4. The quantity cannot exceed available inventory.
            5. The quantity cannot exceed the variant purchase limit,
               when a purchase limit is configured.
            6. If the requested quantity exceeds the effective
               maximum, it is clamped to that maximum.
            7. The CartItem is never deleted.

        Returns:
            tuple:
                (
                    cart_item,
                    quantity_limit_reached,
                )

        Updating a CartItem does not reserve inventory.
        Inventory reservation happens during the
        checkout/order flow.
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
        # Determine maximum allowed quantity
        # ---------------------------------------------------------

        max_quantity = available_quantity

        if variant.purchase_limit is not None:
            max_quantity = min(
                available_quantity,
                variant.purchase_limit,
            )

        # ---------------------------------------------------------
        # Check quantity limit
        # ---------------------------------------------------------

        quantity_limit_reached = (
            quantity > max_quantity
        )

        # ---------------------------------------------------------
        # Calculate new quantity
        # ---------------------------------------------------------

        new_quantity = min(
            quantity,
            max_quantity,
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