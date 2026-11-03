from rest_framework.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from common.services import QuantityValidator

from ..models import OrderItem

from products.models import Inventory

class OrderItemService:

    @staticmethod
    @transaction.atomic
    def create(
        order,
        variant,
        quantity,
        promotion_data,
    ):

        # ---------------------------------------------------------
        # Validate quantity
        # ---------------------------------------------------------

        quantity_data = QuantityValidator.validate(
            variant=variant,
            quantity=quantity,
        )

        if quantity_data["quantity_limit_reached"]:

            raise ValidationError(
                {
                    "code": "quantity_limit_reached",
                    "items": [
                        {
                            "variant": variant.id,
                            "requested_quantity": (
                                quantity_data["requested_quantity"]
                            ),
                            "allowed_quantity": (
                                quantity_data["quantity"]
                            ),
                            "message": (
                                f"Only "
                                f"{quantity_data['quantity']} "
                                f"units can be purchased."
                            ),
                        }
                    ],
                }
            )

        # ---------------------------------------------------------
        # Get Inventory & Lock Row (Concurrency Protection)
        # ---------------------------------------------------------

        try:
            inventory = Inventory.objects.select_for_update().get(
                variant=variant
            )

        except ObjectDoesNotExist:
            raise ValidationError(
                {
                    "variant": (
                        "This variant is not available."
                    )
                }
            )

        # ---------------------------------------------------------
        # Update Reserved Quantity
        # ---------------------------------------------------------

        inventory.reserved_quantity += quantity
        inventory.clean()  # Triggers model validation (checks if reserved > quantity)
        inventory.save(update_fields=["reserved_quantity", "updated_at"])

        # ---------------------------------------------------------
        # Promotion pricing
        # ---------------------------------------------------------

        unit_price = promotion_data["original_price"]
        discount = promotion_data["discount_amount"]
        final_price = promotion_data["final_price"]

        # ---------------------------------------------------------
        # Calculate OrderItem total
        # ---------------------------------------------------------

        total = final_price * quantity

        # ---------------------------------------------------------
        # Create OrderItem
        # ---------------------------------------------------------

        order_item = OrderItem.objects.create(
            order=order,
            variant=variant,
            quantity=quantity,
            unit_price=unit_price,
            discount=discount,
            total=total,
        )

        return order_item