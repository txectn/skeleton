from rest_framework.exceptions import ValidationError

from .providers import (
    BkashPaymentReconciliationService,
    # NagadPaymentReconciliationService,
    # VisaPaymentReconciliationService,
)

class PaymentReconciliationService:

    PROVIDERS = (
        BkashPaymentReconciliationService,
        # NagadPaymentReconciliationService,
        # VisaPaymentReconciliationService,
    )

    @staticmethod
    def reconcile(payment_attempt):

        provider = payment_attempt.provider

        provider_service = None

        for service in PaymentReconciliationService.PROVIDERS:

            if service.can_handle(provider):
                provider_service = service
                break

        if provider_service is None:
            raise ValidationError(
                {
                    "payment": (
                        "Unsupported payment provider."
                    )
                }
            )

        result = provider_service.reconcile(
            payment_attempt=payment_attempt,
        )

        payment = payment_attempt.payment
        order = payment.order

        # ---------------------------------------------------------
        # Payment Already Paid
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
        # Payment Still Pending
        # ---------------------------------------------------------

        if result["status"] == "pending":

            return {
                "payment_id": payment.id,
                "payment_attempt_id": payment_attempt.id,
                "payment_status": payment.status,
                "order_id": order.id,
                "order_status": order.status,
            }

        # ---------------------------------------------------------
        # Payment Failed
        # ---------------------------------------------------------

        if result["status"] == "failed":

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
        # Payment Successful
        # ---------------------------------------------------------

        if result["status"] == "success":

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

            payment.status = payment.Status.PAID

            payment.save(
                update_fields=[
                    "status",
                    "updated_at",
                ]
            )

            if order.status == order.Status.PENDING:

                order.status = order.Status.CONFIRMED

                order.save(
                    update_fields=[
                        "status",
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

        raise ValidationError(
            {
                "payment": (
                    "Unknown payment reconciliation status."
                )
            }
        )