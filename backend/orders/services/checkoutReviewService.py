from cart.services import UserCartService
from common.services import QuantityValidator

from .checkoutReviewShippingService import CheckoutReviewShippingService

class CheckoutReviewService:

    @staticmethod
    def get_checkout(
        *,
        user,
    ):
        cart = UserCartService.get(
            user=user,
        )

        if cart is None:
            return {
                "items": [],
            }

        cart_items = (
            cart.items.select_related(
                "variant",
                "variant__product",
                "variant__product__shipping_class_rates",
            ).prefetch_related(
                "variant__product__media",
            )
        )

        checkout_items = []

        for cart_item in cart_items:
            quantity_data = QuantityValidator.validate(
                variant=cart_item.variant,
                quantity=cart_item.quantity,
            )

            checkout_items.append(
                {
                    "cart_item": cart_item,
                    "quantity": quantity_data["quantity"],
                }
            )

        profile = user.profile

        checkout_items = CheckoutReviewShippingService.calculate_rates(
            items=checkout_items,
            profile=profile,
        )

        # return {
        #     "items": checkout_items,
        # }

        return checkout_items