from django.db import transaction
from products.models import Inventory

def release_order_inventory(order):
    """
    Releases reserved quantity back to available stock when an order is cancelled or failed.
    """
    with transaction.atomic():
        for item in order.items.select_related("variant__inventory").all():
            try:
                inventory = Inventory.objects.select_for_update().get(
                    variant=item.variant
                )
            except Inventory.DoesNotExist:
                continue

            # Release the reservation
            inventory.reserved_quantity -= item.quantity
            if inventory.reserved_quantity < 0:
                inventory.reserved_quantity = 0

            inventory.save(update_fields=["reserved_quantity", "updated_at"])