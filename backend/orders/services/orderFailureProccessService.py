from django.db import transaction
from django.core.exceptions import ValidationError
from payments.models import Payment, PaymentAttempt
from payments.services import BkashRefundService
from .releaseOrderInventory import release_order_inventory

from ..models import Order

# List of supported refund providers
PROVIDERS = (
    BkashRefundService,
    # NagadRefundService,
)

def process_order_failure(order):
    """
    Handles order failure logic:
    1. If paid online, processes the refund via the payment gateway.
    2. Releases reserved inventory back to available stock.
    3. Updates payment status to REFUNDED (if applicable) and order status to FAILED.
    """

    if order.status != Order.Status.FAILED:
        return

    # 1. Check payment for online refund requirements
    try:
        payment = order.payment
    except Payment.DoesNotExist:
        payment = None

    if payment and payment.method == Payment.Method.ONLINE and payment.status == Payment.Status.PAID:
        
        payment_attempt = (
            payment.attempts
            .filter(status=PaymentAttempt.Status.SUCCESS)
            .order_by("-created_at")
            .first()
        )

        if payment_attempt is None:
            raise ValidationError(
                f"Successful payment attempt not found for Order #{order.id}, but payment is marked paid."
            )

        provider = payment_attempt.provider
        provider_service = None

        for service in PROVIDERS:
            if service.select_service(provider):
                provider_service = service
                break

        if provider_service is None:
            raise ValidationError(f"Unsupported payment provider for Order #{order.id}.")

        # Execute external refund API call FIRST
        result = provider_service.refund(
            payment_attempt=payment_attempt,
        )

        if not result or not result.get("success", False):
            raise ValidationError(f"Order failure processing failed: Gateway refund unsuccessful for Order #{order.id}.")

        payment.status = Payment.Status.REFUNDED
        payment.save(update_fields=["status", "updated_at"])

    # 2. All validations/refunds passed: Release reserved inventory
    release_order_inventory(order)

    # 3. Mark order as failed
    if order.status != Order.Status.FAILED:
        order.status = order.Status.FAILED
        order.save(update_fields=["status", "updated_at"])