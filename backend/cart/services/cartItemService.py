from django.db import transaction
from rest_framework.exceptions import ValidationError

from products.models import Inventory

from ..models import CartItem

class CartItemService:

    @staticmethod
    @transaction.atomic
    def add_item(
        *,
        cart,
        variant,
        quantity,
    ):
        """
        Add a variant to a cart.

        If the variant already exists in the cart,
        increase its quantity.

        Inventory is checked before creating or
        updating the CartItem.

        If the requested quantity exceeds the
        available inventory, the quantity is clamped
        to the maximum available quantity.

        Returns:
            tuple:
                (
                    cart_item,
                    increase_limit_reached,
                )

        Adding an item to the cart does not reserve
        inventory. reserved_quantity is only changed
        during the checkout/order reservation flow.
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
        # Get existing CartItem
        # ---------------------------------------------------------

        cart_item = CartItem.objects.filter(
            cart=cart,
            variant=variant,
        ).first()

        # ---------------------------------------------------------
        # Determine current quantity
        # ---------------------------------------------------------

        current_quantity = (
            cart_item.quantity
            if cart_item is not None
            else 0
        )

        # ---------------------------------------------------------
        # Get available inventory
        # ---------------------------------------------------------

        available_quantity = inventory.available_quantity

        # ---------------------------------------------------------
        # Calculate requested quantity
        # ---------------------------------------------------------

        requested_quantity = (
            current_quantity + quantity
        )

        # ---------------------------------------------------------
        # Check inventory limit
        # ---------------------------------------------------------

        increase_limit_reached = (
            requested_quantity > available_quantity
        )

        # ---------------------------------------------------------
        # Calculate new quantity
        # ---------------------------------------------------------

        new_quantity = min(
            requested_quantity,
            available_quantity,
        )

        # ---------------------------------------------------------
        # Create CartItem
        # ---------------------------------------------------------

        if cart_item is None:

            cart_item = CartItem.objects.create(
                cart=cart,
                variant=variant,
                quantity=new_quantity,
            )

        # ---------------------------------------------------------
        # Update existing CartItem
        # ---------------------------------------------------------

        else:

            cart_item.quantity = new_quantity

            cart_item.save(
                update_fields=[
                    "quantity",
                    "updated_at",
                ],
            )

        return (
            cart_item,
            increase_limit_reached,
        )