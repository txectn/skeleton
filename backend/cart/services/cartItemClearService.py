from django.db import transaction

from ..models import CartItem

class CartItemClearService:

    @staticmethod
    @transaction.atomic
    def clear_items(
        *,
        cart,
    ):
        """
        Remove all CartItems from a cart.

        Rules:
            1. The Cart must already exist.
            2. Delete every CartItem belonging to the cart.
            3. Keep the Cart itself.
            4. Return the number of removed items.

        This service does not:
            - Create a Cart.
            - Delete the Cart.
            - Modify inventory.
            - Reserve inventory.
            - Modify individual quantities.
        """

        # -------------------------------------------------------------
        # Delete all CartItems belonging to the cart
        # -------------------------------------------------------------

        deleted_count, _ = CartItem.objects.filter(
            cart=cart,
        ).delete()

        return deleted_count