from django.utils import timezone
from decimal import Decimal
from django.db import IntegrityError, transaction
from django.utils import timezone

from orders.models import Order
from payments.models import Payment

from ..models import (
    AnalyticalMetrics,
    AnalyticalMetricsSnapshot,
    OrderMetricsRecord,
)

from returns.models import ReturnRequest

class AnalyticalMetricsService:
    # Update analytical metrics
    @staticmethod
    @transaction.atomic
    def update_order_metrics(order_id):

        order = Order.objects.select_for_update().get(
            pk=order_id
        )

        record, _ = OrderMetricsRecord.objects.get_or_create(
            order=order
        )

        # Check whether this order currently qualifies as a sale.
        is_qualified = AnalyticalMetricsService.is_qualified(order)

        # Get the current contribution.
        if is_qualified:
            new_sales = 1
            new_revenue = AnalyticalMetricsService.get_revenue(order)
            new_profit = AnalyticalMetricsService.get_profit(order)
        else:
            new_sales = 0
            new_revenue = 0
            new_profit = 0

        # If the contribution has not changed, do nothing.
        if (
            record.is_qualified == is_qualified
            and (
                not is_qualified
                or (
                    record.total_sales == new_sales
                    and record.total_revenue == new_revenue
                    and record.total_profit == new_profit
                )
            )
        ):
            return

        metrics, _ = AnalyticalMetrics.objects.get_or_create(
            pk=1
        )

        metrics = AnalyticalMetrics.objects.select_for_update().get(
            pk=metrics.pk
        )

        # Remove the previous contribution.
        if record.is_qualified:
            metrics.total_sales -= record.total_sales
            metrics.total_revenue -= record.total_revenue
            metrics.profit -= record.total_profit

        # Add the new contribution.
        if is_qualified:
            metrics.total_sales += new_sales
            metrics.total_revenue += new_revenue
            metrics.profit += new_profit

        metrics.save(
            update_fields=[
                "total_sales",
                "total_revenue",
                "profit",
            ]
        )

        # Save the new contribution for future reversals.
        record.is_qualified = is_qualified
        record.total_sales = new_sales
        record.total_revenue = new_revenue
        record.total_profit = new_profit
        record.processed_at = timezone.now()

        record.save()

    @staticmethod
    def is_qualified(order):
        try:
            payment = order.payment
        except Payment.DoesNotExist:
            return False

        return (
            order.status == Order.Status.DELIVERED
            and payment.status == Payment.Status.PAID
            and not ReturnRequest.objects.filter(
                order=order,
                status=ReturnRequest.Status.COMPLETED,
            ).exists()
        )
    
    @staticmethod
    def get_revenue(order):
        return order.total

    @staticmethod
    def get_profit(order):

        product_cost = sum(
            (
                item.variant.cost_price * item.quantity
                for item in order.items.select_related("variant")
            ),
            Decimal("0.00"),
        )

        profit = (
            order.total
            - product_cost
            - order.shipping_cost
        )

        return profit

    # Create snapshot

    @staticmethod
    def create_snapshot():

        today = timezone.localdate()

        # Prevent duplicate daily snapshots
        if AnalyticalMetricsSnapshot.objects.filter(
            created_at__date=today
        ).exists():
            return None

        metrics = AnalyticalMetrics.objects.first()

        if metrics is None:
            return None

        with transaction.atomic():

            # Check again inside the transaction
            if AnalyticalMetricsSnapshot.objects.filter(
                created_at__date=today
            ).exists():
                return None

            snapshot = AnalyticalMetricsSnapshot.objects.create(
                total_products=metrics.total_products,
                total_sales=metrics.total_sales,
                total_revenue=metrics.total_revenue,
                total_profit=metrics.profit,
            )

            return snapshot



