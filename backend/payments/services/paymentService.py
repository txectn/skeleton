from rest_framework.exceptions import ValidationError

from .providers import CodPaymentService
from .onlinePaymentService import OnlinePaymentService

class PaymentService:

    @staticmethod
    def process(
        user, 
        order, 
        payment_method, 
        provider
    ):

        # ---------------------------------------------------------
        # Validate Order
        # ---------------------------------------------------------

        if order.user_id != user.id:
            raise ValidationError(
                {
                    "order": "This order does not belong to you."
                }
            )

        payment_exists = hasattr(order, "payment")

        if order.status in [
            order.Status.CONFIRMED,
            order.Status.PROCESSING,
            order.Status.SHIPPED,
            order.Status.DELIVERED,
        ] and not payment_exists:
            raise ValidationError(
                {
                    "payment": (
                        "This order has an invalid state because "
                        "it does not have a payment."
                    )
                }
            )


        if order.status == order.Status.CONFIRMED:
            
            order_status = order.status
            payment = order.payment
            attempt = payment.attempts.order_by("-created_at").first()
            provider_or_not = "" if payment.method == payment.Method.COD else attempt.provider
            
            raise ValidationError(
                {
                    "message": (
                        "This order has already been confirmed "
                        "and payment has already been initiated."
                    ),
                    "order_status": order_status,
                    "payment_method": payment.method,
                    "payment_provider": provider_or_not,
                    "payment_status": payment.status,
                }
            )
        
        if order.status == order.Status.PROCESSING:
            
            order_status = order.status
            payment = order.payment
            attempt = payment.attempts.order_by("-created_at").first()
            provider_or_not = "" if payment.method == payment.Method.COD else attempt.provider
            
            raise ValidationError(
                {
                    "message": (
                        "This order is already being processed."
                    ),
                    "order_status": order_status,
                    "payment_method": payment.method,
                    "payment_provider": provider_or_not,
                    "payment_status": payment.status,
                }
            )

        if order.status == order.Status.SHIPPED:
            
            order_status = order.status
            payment = order.payment
            attempt = payment.attempts.order_by("-created_at").first()
            provider_or_not = "" if payment.method == payment.Method.COD else attempt.provider
            
            raise ValidationError(
                {
                    "message": (
                        "This order has already been shipped."
                    ),
                    "order_status": order_status,
                    "payment_method": payment.method,
                    "payment_provider": provider_or_not,
                    "payment_status": payment.status,
                }
            )

        if order.status == order.Status.DELIVERED:
            
            order_status = order.status
            payment = order.payment
            attempt = payment.attempts.order_by("-created_at").first()
            provider_or_not = "" if payment.method == payment.Method.COD else attempt.provider
            
            raise ValidationError(
                {
                    "message": (
                        "This order has already been delivered."
                    ),
                    "order_status": order_status,
                    "payment_method": payment.method,
                    "payment_provider": provider_or_not,
                    "payment_status": payment.status,
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
            provider=provider,
        )