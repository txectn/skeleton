from django.db import transaction
from django.core.exceptions import ValidationError

from products.models import Inventory
from productMetrics.tasks import record_product_sold

def process_order_fulfillment(order):
    """
    Fulfill a delivered, paid order exactly once.

    Decreases physical quantity and releases reserved quantity.
    Records sold quantities after the transaction commits.
    """

    if order.status != order.Status.DELIVERED:
        return

    with transaction.atomic():
        # Lock the order so concurrent requests cannot fulfill it twice.
        locked_order = (
            order.__class__.objects
            .select_for_update()
            .get(pk=order.pk)
        )

        # Recheck status after acquiring the lock.
        if locked_order.status != locked_order.Status.DELIVERED:
            return

        # IMPORTANT:
        # Replace this check if your Payment model uses a different
        # relationship or status value.
        payment = getattr(locked_order, "payment", None)

        if payment is None or payment.status != "paid":
            raise ValidationError(
                "Cannot fulfill an order without confirmed payment."
            )

        items = list(
            locked_order.items.select_related(
                "variant__product"
            ).all()
        )

        inventory_rows = []

        # Lock inventory rows in a consistent order.
        variant_ids = sorted({
            item.variant_id for item in items
        })

        inventories = {
            inventory.variant_id: inventory
            for inventory in Inventory.objects.select_for_update()
            .filter(variant_id__in=variant_ids)
            .order_by("variant_id")
        }

        for item in items:
            inventory = inventories.get(item.variant_id)

            if inventory is None:
                raise ValidationError(
                    f"Inventory not found for variant {item.variant.sku}."
                )

            if (
                inventory.quantity < item.quantity
                or inventory.reserved_quantity < item.quantity
            ):
                raise ValidationError(
                    f"Insufficient stock or reserved quantity for "
                    f"variant {item.variant.sku}."
                )

            inventory.quantity -= item.quantity
            inventory.reserved_quantity -= item.quantity

            inventory.clean()
            inventory_rows.append(inventory)

        for inventory in inventory_rows:
            inventory.save(
                update_fields=[
                    "quantity",
                    "reserved_quantity",
                    "updated_at",
                ]
            )

        # Schedule metrics updates only after a successful commit.
        for item in items:
            product_id = item.variant.product_id
            quantity = item.quantity

            transaction.on_commit(
                lambda p_id=product_id, qty=quantity: (
                    record_product_sold.delay(
                        product_id=p_id,
                        quantity=qty,
                    )
                )
            )
