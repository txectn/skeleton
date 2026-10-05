from django.db import transaction
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

    @classmethod
    def reconcile(cls, payment_attempt):

        # ---------------------------------------------------------
        # Validate Payment Attempt
        # ---------------------------------------------------------

        if payment_attempt is None:
            raise ValidationError(
                {
                    "payment": (
                        "Payment attempt is required."
                    )
                }
            )

        payment = payment_attempt.payment
        order = payment.order

        # ---------------------------------------------------------
        # Validate Payment Attempt State
        # ---------------------------------------------------------

        if (
            payment_attempt.status
            != payment_attempt.Status.PENDING
        ):
            raise ValidationError(
                {
                    "message": (
                        "This payment attempt has already "
                        "been processed."
                    ),
                    "payment_attempt_status": (
                        payment_attempt.status
                    ),
                }
            )

        # ---------------------------------------------------------
        # Validate Payment State
        # ---------------------------------------------------------

        if payment.status != payment.Status.PENDING:
            raise ValidationError(
                {
                    "message": (
                        "This payment is not pending."
                    ),
                    "payment_status": payment.status,
                }
            )

        # ---------------------------------------------------------
        # Validate Order State
        # ---------------------------------------------------------

        if order.status != order.Status.PENDING:
            raise ValidationError(
                {
                    "message": (
                        "The order is not in a pending state."
                    ),
                    "order_status": order.status,
                }
            )

        # ---------------------------------------------------------
        # Find Provider Service
        # ---------------------------------------------------------

        provider = payment_attempt.provider

        provider_service = None

        for service in cls.PROVIDERS:

            if service.can_handle(provider):
                provider_service = service
                break

        if provider_service is None:
            raise ValidationError(
                {
                    "payment": (
                        "Unsupported payment provider."
                    ),
                    "provider": provider,
                }
            )

        # ---------------------------------------------------------
        # Reconcile With Provider
        # ---------------------------------------------------------

        result = provider_service.reconcile(
            payment_attempt=payment_attempt,
        )

        # ---------------------------------------------------------
        # Validate Provider Result
        # ---------------------------------------------------------

        if not isinstance(result, dict):
            raise ValidationError(
                {
                    "payment": (
                        "Invalid payment reconciliation result."
                    )
                }
            )

        status = result.get("status")

        if status not in (
            "success",
            "failed",
            "pending",
        ):
            raise ValidationError(
                {
                    "payment": (
                        "Unknown payment reconciliation status."
                    ),
                    "status": status,
                }
            )

        # ---------------------------------------------------------
        # Payment Still Pending
        # ---------------------------------------------------------

        if status == "pending":

            return cls._build_result(
                payment_attempt=payment_attempt,
                payment=payment,
                order=order,
            )

        # ---------------------------------------------------------
        # Payment Failed
        # ---------------------------------------------------------

        if status == "failed":

            cls._mark_failed(
                payment_attempt=payment_attempt,
                result=result,
            )

            return cls._build_result(
                payment_attempt=payment_attempt,
                payment=payment,
                order=order,
            )

        # ---------------------------------------------------------
        # Payment Successful
        # ---------------------------------------------------------

        if status == "success":

            cls._mark_success(
                payment_attempt=payment_attempt,
                payment=payment,
                order=order,
                result=result,
            )

            return cls._build_result(
                payment_attempt=payment_attempt,
                payment=payment,
                order=order,
            )

        raise ValidationError(
            {
                "payment": (
                    "Unable to reconcile payment."
                )
            }
        )

    # =============================================================
    # State Changes
    # =============================================================

    @staticmethod
    @transaction.atomic
    def _mark_failed(
        payment_attempt,
        result,
    ):
        payment_attempt.status = (
            payment_attempt.Status.FAILED
        )

        transaction_id = result.get(
            "transaction_id"
        )

        if transaction_id:
            payment_attempt.transaction_id = (
                transaction_id
            )

            payment_attempt.save(
                update_fields=[
                    "status",
                    "transaction_id",
                    "updated_at",
                ]
            )

        else:
            payment_attempt.save(
                update_fields=[
                    "status",
                    "updated_at",
                ]
            )

    @staticmethod
    @transaction.atomic
    def _mark_success(
        payment_attempt,
        payment,
        order,
        result,
    ):
        # ---------------------------------------------------------
        # Payment Attempt
        # ---------------------------------------------------------

        payment_attempt.status = (
            payment_attempt.Status.SUCCESS
        )

        transaction_id = result.get(
            "transaction_id"
        )

        if transaction_id:
            payment_attempt.transaction_id = (
                transaction_id
            )

            payment_attempt.save(
                update_fields=[
                    "status",
                    "transaction_id",
                    "updated_at",
                ]
            )

        else:
            payment_attempt.save(
                update_fields=[
                    "status",
                    "updated_at",
                ]
            )

        # ---------------------------------------------------------
        # Payment
        # ---------------------------------------------------------

        payment.status = payment.Status.PAID

        payment.save(
            update_fields=[
                "status",
                "updated_at",
            ]
        )

        # ---------------------------------------------------------
        # Order
        # ---------------------------------------------------------

        if order.status == order.Status.PENDING:

            order.status = order.Status.CONFIRMED

            order.save(
                update_fields=[
                    "status",
                    "updated_at",
                ]
            )

    # =============================================================
    # Response
    # =============================================================

    @staticmethod
    def _build_result(
        payment_attempt,
        payment,
        order,
    ):
        return {
            "payment_id": payment.id,
            "payment_attempt_id": payment_attempt.id,
            "payment_status": payment.status,
            "payment_attempt_status": (
                payment_attempt.status
            ),
            "order_id": order.id,
            "order_status": order.status,
        }