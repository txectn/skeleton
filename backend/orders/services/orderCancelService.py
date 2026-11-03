from rest_framework.exceptions import ValidationError
from django.db import transaction

from ..models import Order
from payments.models import Payment, PaymentAttempt
from payments.services import BkashRefundService
from .releaseOrderInventory import release_order_inventory  # Import the release function

class OrderCancelService:

    PROVIDERS = (
        BkashRefundService,
        # NagadRefundService
    )

    @classmethod
    @transaction.atomic
    def cancel(cls, *, user, order):

        # 1. Check if order belongs to user
        if order.user_id != user.id:
            raise ValidationError(
                {
                    "message": "This order does not belong to you.",
                }
            )

        # 2. Check if cancelled or not
        if order.status == Order.Status.CANCELLED:
            raise ValidationError(
                {
                    "message": "This order is already cancelled.",
                    "order_id": order.id,
                    "order_status": order.status,
                }
            )

        # 3. Check if order is failed
        if order.status == Order.Status.FAILED:
            raise ValidationError(
                {
                    "message": "This order is failed.",
                    "order_id": order.id,
                    "order_status": order.status,
                }
            )

        # 4. Check if order can be cancelled
        if order.status not in (
            Order.Status.PENDING,
            Order.Status.CONFIRMED,
            Order.Status.PROCESSING,
        ):
            raise ValidationError(
                {
                    "message": "This order cannot be cancelled.",
                    "order_id": order.id,
                    "order_status": order.status,
                }
            )

        # Get payment
        try:
            payment = order.payment
        except Payment.DoesNotExist:
            payment = None

        # 5. Handle Online Payment Refunds FIRST (External API can fail here)
        if payment and payment.method == Payment.Method.ONLINE and payment.status == Payment.Status.PAID:

            payment_attempt = (
                payment.attempts
                .filter(status=PaymentAttempt.Status.SUCCESS)
                .order_by("-created_at")
                .first()
            )

            if payment_attempt is None:
                raise ValidationError(
                    {
                        "message": "Successful payment attempt not found.",
                        "order_id": order.id,
                        "order_status": order.status,
                    }
                )

            provider = payment_attempt.provider
            provider_service = None

            for service in cls.PROVIDERS:
                if service.select_service(provider):
                    provider_service = service
                    break

            if provider_service is None:
                raise ValidationError(
                    {
                        "message": "Unsupported payment provider.",
                        "order_id": order.id,
                        "order_status": order.status,
                    }
                )

            result = provider_service.refund(
                payment_attempt=payment_attempt,
            )

            if not result or not result.get("success", False):
                raise ValidationError(
                    {
                        "message": "This order cannot be cancelled & refund failed.",
                        "order_id": order.id,
                        "order_status": order.status,
                    }
                )

            payment.status = Payment.Status.REFUNDED
            payment.save(update_fields=["status", "updated_at"])

        # -------------------------------------------------------------
        # 6. ALL CHECKS & REFUNDS PASSED: Release inventory & cancel order once for all cases
        # -------------------------------------------------------------
        release_order_inventory(order)

        order.status = Order.Status.CANCELLED
        order.save(update_fields=["status", "updated_at"])

        return {
            "message": "Order cancelled successfully.",
            "order_id": order.id,
            "order_status": order.status,
        }