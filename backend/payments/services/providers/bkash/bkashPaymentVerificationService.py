from django.db import transaction
from rest_framework.exceptions import ValidationError

from .bkashPaymentExecutionService import (
    BkashPaymentExecutionService,
)

class BkashPaymentVerificationService:
    """Handles bKash payment verification flow."""

    @classmethod
    def verify_payment(cls, user, data):

        payment_id = data["paymentID"]
        callback_status = data["status"]

        # Callback Validation
        if callback_status != "success":
            raise ValidationError(
                {
                    "payment": (
                        "The bKash payment was not completed."
                    ),
                    "status": callback_status,
                }
            )

        # Execute Payment
        result = BkashPaymentExecutionService.execute_payment(
            user=user,
            payment_id=payment_id,
        )

        payment_attempt = result["payment_attempt"]
        payment = result["payment"]
        order = result["order"]

        # Already Paid
        if payment.status == payment.Status.PAID:
            return {
                "message": "Payment has already been completed.",
                "payment_status": payment.status,
                "order_status": order.status,
            }

        # Invalid Attempt State
        if (
            payment_attempt.status
            == payment_attempt.Status.PAID
        ):
            return {
                "message": (
                    "Payment attempt has already been completed."
                ),
                "payment_status": payment.status,
                "order_status": order.status,
            }

        if (
            payment_attempt.status
            == payment_attempt.Status.FAILED
        ):
            raise ValidationError(
                {
                    "payment": (
                        "This payment attempt has already failed."
                    )
                }
            )

        # Save Payment State
        with transaction.atomic():

            payment_attempt.status = (
                payment_attempt.Status.PAID
            )

            payment_attempt.save(
                update_fields=[
                    "status",
                    "updated_at",
                ]
            )

            payment.status = payment.Status.PAID

            payment.save(
                update_fields=[
                    "status",
                    "updated_at",
                ]
            )

            order.status = order.Status.CONFIRMED

            order.save(
                update_fields=[
                    "status",
                    "updated_at",
                ]
            )

        return {
            "message": "Payment completed successfully.",
            "payment_status": payment.status,
            "order_status": order.status,
            "payment_id": result["payment_id"],
            "trx_id": result["trx_id"],
            "amount": result["amount"],
            "currency": result["currency"],
            "transaction_status": result["transaction_status"],
        }




'''
Frontend
   │
   │ POST /api/payment/verify/bkash/
   │
   │ {
   │     paymentID,
   │     status
   │ }
   ▼
BkashVerifyPaymentView
   │
   │ Validate request data
   ▼
BkashVerifyPaymentSerializer
   │
   │ validated_data
   ▼
BkashPaymentVerificationService
   │
   ├── 1. Get paymentID
   │       │
   │       └── data["paymentID"]
   │
   ├── 2. Get callback status
   │       │
   │       └── data["status"]
   │
   ├── 3. Check callback status
   │       │
   │       ├── success ────────────────┐
   │       │                           │
   │       └── anything else → Error  │
   │                                   ▼
   ├── 4. Find PaymentAttempt
   │       │
   │       │ provider_payment_id = paymentID
   │       │ provider = bkash
   │       │ order.user = current user
   │       ▼
   │
   ├── 5. Get related objects
   │       │
   │       ├── PaymentAttempt
   │       ├── Payment
   │       └── Order
   │
   ├── 6. Check current payment state
   │       │
   │       ├── Payment already PAID
   │       │       └── return already completed
   │       │
   │       ├── Attempt already PAID
   │       │       └── return already completed
   │       │
   │       └── Attempt FAILED
   │               └── reject
   │
   ├── 7. Get bKash ID Token
   │       │
   │       └── BkashTokenService
   │
   ├── 8. Execute Payment
   │       │
   │       │ POST /tokenized/checkout/execute
   │       │
   │       │ {
   │       │     "paymentID": paymentID
   │       │ }
   │       ▼
   │
   ├── 9. Validate bKash response
   │       │
   │       ├── statusCode == "0000"
   │       │
   │       ├── paymentID matches
   │       │
   │       ├── transactionStatus == "Completed"
   │       │
   │       ├── trxID exists
   │       │
   │       └── amount matches Order.total
   │
   ├── 10. Database transaction
   │       │
   │       ├── PaymentAttempt → PAID
   │       │
   │       ├── Payment → PAID
   │       │
   │       └── Order → CONFIRMED
   │
   └── 11. Return successful response
           │
           ├── payment_status
           ├── order_status
           ├── payment_id
           ├── trx_id
           ├── amount
           └── currency
'''