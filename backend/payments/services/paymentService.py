from rest_framework.exceptions import ValidationError

from .providers import CodPaymentService
from .onlinePaymentService import OnlinePaymentService

class PaymentService:

    @staticmethod
    def process(user, order, payment_method):

        # ---------------------------------------------------------
        # Validate Order
        # ---------------------------------------------------------

        if order.user_id != user.id:
            raise ValidationError(
                {
                    "order": "This order does not belong to you."
                }
            )

        if order.status == order.Status.CONFIRMED:
            raise ValidationError(
                {
                    "order": (
                        "This order has already been confirmed "
                        "and payment has already been initiated."
                    )
                }
            )

        if order.status == order.Status.PROCESSING:
            raise ValidationError(
                {
                    "order": (
                        "This order is already being processed."
                    )
                }
            )

        if order.status == order.Status.SHIPPED:
            raise ValidationError(
                {
                    "order": (
                        "This order has already been shipped."
                    )
                }
            )

        if order.status == order.Status.DELIVERED:
            raise ValidationError(
                {
                    "order": (
                        "This order has already been delivered."
                    )
                }
            )

        if order.status == order.Status.CANCELLED:
            raise ValidationError(
                {
                    "order": (
                        "This order has been cancelled "
                        "and cannot be processed."
                    ),
                }
            )

        # ---------------------------------------------------------
        # Payment Method
        # ---------------------------------------------------------

        if payment_method == "cod":

            return CodPaymentService.process(
                order=order,
            )

        # ---------------------------------------------------------
        # Online Payment
        # ---------------------------------------------------------

        return OnlinePaymentService.process(
            order=order,
            provider=payment_method,
        )