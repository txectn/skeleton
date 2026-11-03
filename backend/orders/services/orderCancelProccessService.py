from django.core.exceptions import ValidationError
from payments.models import Payment, PaymentAttempt
from payments.services import BkashRefundService
from .releaseOrderInventory import release_order_inventory

from ..models import Order

PROVIDERS = (
    BkashRefundService,
    # NagadRefundService,
)

def process_order_cancellation(order):
    """
    Handles complete order cancellation logic:
    1. If paid online, processes the refund via the payment gateway first.
    2. Releases reserved inventory back to available stock.
    3. Updates payment status to REFUNDED and order status to CANCELLED.
    """

    if order.status != Order.Status.CANCELLED:
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
            raise ValidationError(f"Order cancellation failed: Gateway refund unsuccessful for Order #{order.id}.")

        payment.status = Payment.Status.REFUNDED
        payment.save(update_fields=["status", "updated_at"])

    # 2. All validations/refunds passed: Release reserved inventory
    release_order_inventory(order)

    # 3. Mark order as cancelled
    if order.status != Order.Status.CANCELLED:
        order.status = order.Status.CANCELLED
        order.save(update_fields=["status", "updated_at"])