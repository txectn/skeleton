from django.db import models

from orders.models import Order

class ReturnRequest(models.Model):

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        PREPARING = "preparing", "Preparing"
        INSPECTING = "inspecting", "Inspecting"
        RETURNING = "returning", "Returning"
        COMPLETED = "completed", "Completed"
        FAILED = "failed", "Failed"
        CANCELLED = "cancelled", "Cancelled"

    class Decision(models.TextChoices):
        PENDING = "pending", "Pending"
        BUSINESS_FAULT = "business_fault", "Business Fault"
        CUSTOMER_RETURN = "customer_return", "Customer Return"
        INVALID_RETURN = "invalid_return", "Invalid Return"
        CUSTOMER_CANCELLED = "customer_cancelled", "Customer Cancelled"

    class Reason(models.TextChoices):
        CHANGED_MIND = "changed_mind", "Changed my mind"
        ORDERED_BY_MISTAKE = "ordered_by_mistake", "Ordered by mistake"
        WRONG_PRODUCT = "wrong_product", "Wrong product received"
        DAMAGED = "damaged", "Product is damaged"
        FAKE = "fake", "Product is fake / not authentic"
        NOT_AS_DESCRIBED = "not_as_described", "Product is not as described"
        MISSING_ITEM = "missing_item", "Item is missing"
        OTHER = "other", "Other"

    class MoneyRefundStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        REFUNDED = "refunded", "Refunded"
        REFUND_FAILED = "refund_failed", "Refund Failed"
        REFUND_CANCELLED = "refund_cancelled", "Refund Cancelled"

    order = models.ForeignKey(
        Order,
        on_delete=models.PROTECT,
        related_name="return_requests",
    )

    reason = models.CharField(
        max_length=30,
        choices=Reason.choices,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )

    decision = models.CharField(
        max_length=20,
        choices=Decision.choices,
        default=Decision.PENDING,
    )

    money_refund_status = models.CharField(
        max_length=20,
        choices=MoneyRefundStatus.choices,
        default=MoneyRefundStatus.PENDING,
    )

    customer_note = models.TextField(
        blank=True,
    )

    inspector_note = models.TextField(
        blank=True,
    )

    return_charge = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    refund_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return f"Return Request #{self.pk} - Order #{self.order_id}"