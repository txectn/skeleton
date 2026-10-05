from django.db import transaction
from rest_framework.exceptions import ValidationError

from ..models import Payment, PaymentAttempt
from .providers import CodPaymentService
from .onlinePaymentService import OnlinePaymentService

class PaymentMethodChangeService:

    ALLOWED_ORDER_STATUSES = (
        "pending",
        "processing",
        "confirmed",
    )

    @staticmethod
    def change_payment_method(
        user,
        order,
        payment_method,
        provider=None,
    ):
        # ---------------------------------------------------------
        # Order Ownership
        # ---------------------------------------------------------

        if order.user_id != user.id:
            raise ValidationError(
                {
                    "order": (
                        "You do not have permission "
                        "to change this order's payment method."
                    )
                }
            )

        # ---------------------------------------------------------
        # Get Payment
        # ---------------------------------------------------------

        payment = Payment.objects.filter(
            order=order,
        ).first()

        # ---------------------------------------------------------
        # Order Status
        # ---------------------------------------------------------

        if order.status not in PaymentMethodChangeService.ALLOWED_ORDER_STATUSES:
            raise ValidationError(
                {
                    "message": (
                        "Cannot change payment method "
                        "for this order."
                    ),
                    "order_status": order.status,
                    "payment_method": payment_method,
                    "payment_status": payment.status,
                }
            )

        # ---------------------------------------------------------
        # Payment Status
        # ---------------------------------------------------------

        if payment and payment.status in (
            Payment.Status.PAID,
            Payment.Status.FAILED,
        ):
            raise ValidationError(
                {
                    "message": (
                        "Cannot change payment method "
                        "for this payment."
                    ),
                    "order_status": order.status,
                    "payment_method": payment.method,
                    "payment_status": payment.status,
                }
            )

        # ---------------------------------------------------------
        # Existing Pending Payment Attempt
        # ---------------------------------------------------------

        pending_attempt = None

        if payment:
            pending_attempt = payment.attempts.filter(
                status=PaymentAttempt.Status.PENDING,
            ).order_by("-created_at").first()

        # ---------------------------------------------------------
        # Provider Validation
        # ---------------------------------------------------------

        if payment_method == Payment.Method.ONLINE and not provider:
            raise ValidationError(
                {
                    "message": (
                        "Provider is required for online payment."
                    ),
                    "order_status": order.status,
                    "payment_method": payment_method,
                    "payment_status": payment.status,
                }
            )

        # ---------------------------------------------------------
        # Same Payment Method
        # ---------------------------------------------------------

        # if payment and payment.method == payment_method:
        #     raise ValidationError(
        #         {
        #             "message": (
        #                 "This payment method is already selected."
        #             ),
        #             "order_status": order.status,
        #             "payment_method": payment_method,
        #             "payment_status": payment.status,
        #         }
        #     )

        # ---------------------------------------------------------
        # Switch Payment Method
        # ---------------------------------------------------------

        if payment_method == Payment.Method.COD:

            # -----------------------------------------------------
            # Invalidate Existing Pending Attempt
            # -----------------------------------------------------

            if pending_attempt:
                pending_attempt.status = PaymentAttempt.Status.FAILED
                pending_attempt.save(
                    update_fields=[
                        "status",
                        "updated_at",
                    ]
                )

            # -----------------------------------------------------
            # COD Payment
            # -----------------------------------------------------

            return CodPaymentService.process(
                order=order,
            )

        # ---------------------------------------------------------
        # Switch To Online Payment
        # ---------------------------------------------------------

        if payment:
            payment.method = payment_method
            payment.save(
                update_fields=[
                    "method",
                    "updated_at",
                ]
            )

        # ---------------------------------------------------------
        # Change Order Status
        # ---------------------------------------------------------

        order.status = order.Status.PENDING
        order.save(
            update_fields=[
                "status",
                "updated_at",
            ]
        )

        # ---------------------------------------------------------
        # Invalidate Existing Pending Attempt
        # ---------------------------------------------------------

        if pending_attempt:
            pending_attempt.status = PaymentAttempt.Status.FAILED
            pending_attempt.save(
                update_fields=[
                    "status",
                    "updated_at",
                ]
            )

        # ---------------------------------------------------------
        # Online Payment
        # ---------------------------------------------------------

        return OnlinePaymentService.process(
            order=order,
            provider=provider,
        )