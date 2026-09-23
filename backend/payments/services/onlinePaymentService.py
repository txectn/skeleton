from rest_framework.exceptions import ValidationError

from ..models import Payment, PaymentAttempt
from .providers import (
    BkashPaymentService,
    # NagadPaymentService,
    # VisaPaymentService,
)

class OnlinePaymentService:

    @staticmethod
    def process(order, provider):

        # ---------------------------------------------------------
        # Payment Provider
        # ---------------------------------------------------------

        if provider == "bkash":
            provider_service = BkashPaymentService

        # elif provider == "nagad":
        #     provider_service = NagadPaymentService

        # elif provider == "visa":
        #     provider_service = VisaPaymentService

        else:
            raise ValidationError(
                {
                    "provider": (
                        "Unsupported payment provider."
                    )
                }
            )

        # ---------------------------------------------------------
        # Get or Create Payment
        # ---------------------------------------------------------

        payment, created = Payment.objects.get_or_create(
            order=order,
            defaults={
                "method": Payment.Method.ONLINE,
                "status": Payment.Status.PENDING,
            },
        )

        # ---------------------------------------------------------
        # Validate Payment Method
        # ---------------------------------------------------------

        if payment.method != Payment.Method.ONLINE:
            raise ValidationError(
                {
                    "payment": (
                        "This order is not configured "
                        "for online payment."
                    )
                }
            )

        # ---------------------------------------------------------
        # Check Payment Status
        # ---------------------------------------------------------

        if payment.status == Payment.Status.PAID:
            raise ValidationError(
                {
                    "payment": (
                        "This order has already been paid."
                    )
                }
            )

        # ---------------------------------------------------------
        # Create Payment Attempt
        # ---------------------------------------------------------

        payment_attempt = PaymentAttempt.objects.create(
            payment=payment,
            provider=provider,
            status=PaymentAttempt.Status.PENDING,
        )

        # ---------------------------------------------------------
        # Create Provider Payment
        # ---------------------------------------------------------

        result = provider_service.create_payment(
            order=order,
            payment=payment,
            payment_attempt=payment_attempt,
        )

        # ---------------------------------------------------------
        # Return Payment Result
        # ---------------------------------------------------------

        return {
            "payment_id": payment.id,
            "payment_attempt_id": payment_attempt.id,
            "payment_method": payment.method,
            "payment_status": payment.status,
            "provider": provider,
            **result,
        }

