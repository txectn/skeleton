from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError

class QuantityValidator:

    @staticmethod
    def validate(
        *,
        variant,
        quantity,
    ):
        """
        Validate and calculate the allowed quantity for a variant.

        The maximum allowed quantity is determined by the lower of:
            - available inventory
            - variant purchase limit, when configured

        This method does not modify any database records.

        Returns:
            dict: Quantity validation result.
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
        # Get inventory
        # ---------------------------------------------------------

        try:
            inventory = variant.inventory

        except ObjectDoesNotExist:
            raise ValidationError(
                {
                    "variant": (
                        "This variant is not available."
                    )
                }
            )

        # ---------------------------------------------------------
        # Determine maximum allowed quantity
        # ---------------------------------------------------------

        available_quantity = inventory.available_quantity

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
        # Calculate allowed quantity
        # ---------------------------------------------------------

        allowed_quantity = min(
            quantity,
            max_quantity,
        )

        return {
            "quantity": allowed_quantity,
            "requested_quantity": quantity,
            # "max_quantity": max_quantity,
            "quantity_limit_reached": quantity_limit_reached,
            "purchase_limit": variant.purchase_limit,
            # "available_quantity": available_quantity,
        }