from django.db import transaction

from ..models import Order

from promotions.services import PromotionService
from .orderItemService import OrderItemService
from .orderPriceService import OrderPriceService
from .orderShippingService import OrderShippingService

class OrderService:

    @staticmethod
    @transaction.atomic
    def create_order(user, items):

        # ---------------------------------------------------------
        # Validate checkout items / quantities
        # ---------------------------------------------------------

        # items already contains:
        #
        # [
        #     {
        #         "variant": Variant(...),
        #         "quantity": 2,
        #     },
        #     ...
        # ]
        #
        # Quantity validation will be handled by the appropriate
        # service and its result will be returned here.

        # ---------------------------------------------------------
        # Shipping information
        # ---------------------------------------------------------

        shipping_data = OrderShippingService.get_shipping_information(
            user=user,
        )

        # ---------------------------------------------------------
        # Create Order
        # ---------------------------------------------------------

        order = Order.objects.create(
            user=user,
            status=Order.Status.PENDING,

            subtotal=0,
            discount=0,
            shipping=0,
            total=0,
            
            shipping_address=shipping_data["shipping_address"],
            shipping_city=shipping_data["shipping_city"],
            shipping_region=shipping_data["shipping_region"],
            shipping_country=shipping_data["shipping_country"],
            phone_number=shipping_data["phone_number"],
        )

        # ---------------------------------------------------------
        # Order Items
        # ---------------------------------------------------------

        for item in items:

            promotion_data = (
                PromotionService.get_variant_promotion(
                    variant=item["variant"],
                )
            )

            OrderItemService.create(
                order=order,
                variant=item["variant"],
                quantity=item["quantity"],
                promotion_data=promotion_data,
            )

        # ---------------------------------------------------------
        # Shipping
        # ---------------------------------------------------------

        shipping = OrderShippingService.calculate(
            order=order,
        )

        # ---------------------------------------------------------
        # Order Price
        # ---------------------------------------------------------

        price_data = OrderPriceService.calculate(
            order=order,
            shipping=shipping,
        )

        # ---------------------------------------------------------
        # Final Order totals
        # ---------------------------------------------------------

        order.subtotal = price_data["subtotal"]
        order.discount = price_data["discount"]
        order.shipping = shipping
        order.total = price_data["total"]

        order.save(
            update_fields=[
                "subtotal",
                "discount",
                "shipping",
                "total",
                "updated_at",
            ]
        )

        return order





