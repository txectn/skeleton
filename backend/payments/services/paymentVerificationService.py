from django.db import transaction
from rest_framework.exceptions import ValidationError

from .providers import (
    BkashPaymentVerificationService,
    # NagadPaymentVerificationService,
    # VisaPaymentVerificationService,
)

class PaymentVerificationService:

    PROVIDERS = (
        BkashPaymentVerificationService,
        # NagadPaymentVerificationService,
        # VisaPaymentVerificationService,
    )

    @staticmethod
    @transaction.atomic
    def process_webhook(data):

        # ---------------------------------------------------------
        # Identify Payment Provider
        # ---------------------------------------------------------

        provider_service = None

        for service in PaymentVerificationService.PROVIDERS:

            if service.can_handle(data):
                provider_service = service
                break

        if provider_service is None:
            raise ValidationError(
                {
                    "payment": (
                        "Unable to identify the payment provider."
                    )
                }
            )

        # ---------------------------------------------------------
        # Verify Payment With Provider
        # ---------------------------------------------------------

        result = provider_service.verify(
            data=data,
        )

        payment_attempt = result["payment_attempt"]
        payment = payment_attempt.payment
        order = payment.order

        # ---------------------------------------------------------
        # Already Paid
        # ---------------------------------------------------------

        if payment.status == payment.Status.PAID:
            return {
                "payment_id": payment.id,
                "payment_attempt_id": payment_attempt.id,
                "payment_status": payment.status,
                "order_id": order.id,
                "order_status": order.status,
            }

        # ---------------------------------------------------------
        # Payment Verification Failed
        # ---------------------------------------------------------

        if not result["success"]:

            payment_attempt.status = (
                payment_attempt.Status.FAILED
            )

            if result.get("transaction_id"):
                payment_attempt.transaction_id = (
                    result["transaction_id"]
                )

            payment_attempt.save(
                update_fields=[
                    "status",
                    "transaction_id",
                    "updated_at",
                ]
            )

            return {
                "payment_id": payment.id,
                "payment_attempt_id": payment_attempt.id,
                "payment_status": payment.status,
                "order_id": order.id,
                "order_status": order.status,
            }

        # ---------------------------------------------------------
        # Payment Verification Successful
        # ---------------------------------------------------------

        payment_attempt.status = (
            payment_attempt.Status.SUCCESS
        )

        if result.get("transaction_id"):
            payment_attempt.transaction_id = (
                result["transaction_id"]
            )

        payment_attempt.save(
            update_fields=[
                "status",
                "transaction_id",
                "updated_at",
            ]
        )

        # ---------------------------------------------------------
        # Mark Payment as Paid
        # ---------------------------------------------------------

        payment.status = payment.Status.PAID

        payment.save(
            update_fields=[
                "status",
                "updated_at",
            ]
        )

        # ---------------------------------------------------------
        # Confirm Order
        # ---------------------------------------------------------

        if order.status == order.Status.PENDING:

            order.status = order.Status.CONFIRMED

            order.save(
                update_fields=[
                    "status",
                    "updated_at",
                ]
            )

        # ---------------------------------------------------------
        # Return Result
        # ---------------------------------------------------------

        return {
            "payment_id": payment.id,
            "payment_attempt_id": payment_attempt.id,
            "payment_status": payment.status,
            "order_id": order.id,
            "order_status": order.status,
        }

    

'''
PaymentWebhookView
        │
        ▼
PaymentVerificationService
        │
        ├── identify provider
        │
        ├── identify payment
        │
        └── select verification service
                │
        ┌───────┼────────┐
        ▼       ▼        ▼
     bKash    Nagad     Visa
     Verify   Verify    Verify
        │       │        │
        └───────┼────────┘
                ▼
       Common verification result
                │
                ▼
       Update PaymentAttempt
                │
                ▼
          Update Payment
                │
                ▼
          Update Order
'''