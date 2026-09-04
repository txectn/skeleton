from django.db import transaction
from rest_framework.exceptions import ValidationError

from ..models import CartItem

class CartItemRemoveService:

    @staticmethod
    @transaction.atomic
    def remove_item(
        *,
        cart,
        variant,
    ):
        """
        Remove an existing CartItem from a cart.

        Rules:
            1. The CartItem must already exist.
            2. The CartItem is identified by cart and variant.
            3. If the CartItem does not exist, raise a validation error.
            4. Delete the CartItem.
            5. Return the removed variant ID.

        This service does not:
            - Create a CartItem.
            - Modify inventory.
            - Modify quantity.
            - Reserve inventory.
            - Create a Cart.
        """

        # -------------------------------------------------------------
        # Find CartItem
        # -------------------------------------------------------------

        try:
            cart_item = CartItem.objects.get(
                cart=cart,
                variant=variant,
            )

        except CartItem.DoesNotExist:

            raise ValidationError({
                "variant": "This item does not exist in the cart.",
            })

        # -------------------------------------------------------------
        # Store variant ID before deleting the CartItem
        # -------------------------------------------------------------

        variant_id = cart_item.variant_id

        # -------------------------------------------------------------
        # Remove CartItem
        # -------------------------------------------------------------

        cart_item.delete()

        # -------------------------------------------------------------
        # Return removed variant ID
        # -------------------------------------------------------------

        return variant_id