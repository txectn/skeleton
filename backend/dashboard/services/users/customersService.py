from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db.models import (
    Count,
    DecimalField,
    OuterRef,
    Q,
    Subquery,
    Sum,
    Value,
)
from django.db.models.functions import Coalesce

from orders.models import Order

User = get_user_model()

class CustomersService:

    @staticmethod
    def get_customers():
        latest_order = Order.objects.filter(
            user_id=OuterRef("pk"),
        ).order_by("-created_at", "-id")

        return (
            User.objects
            .annotate(
                orders_count=Count("orders", distinct=True),
                total_spent=Coalesce(
                    Sum(
                        "orders__total",
                        filter=Q(
                            orders__status=Order.Status.DELIVERED,
                            orders__payment__status="paid",
                        ),
                    ),
                    Value(Decimal("0.00")),
                    output_field=DecimalField(
                        max_digits=12,
                        decimal_places=2,
                    ),
                ),
                latest_phone=Subquery(
                    latest_order.values("phone_number")[:1]
                ),
            )
            .order_by("-id")
        )

    @staticmethod
    def serialize_customers(customers):
        return [
            {
                "id": customer.id,
                "name": (
                    customer.get_full_name()
                    or customer.username
                    or customer.email
                    or ""
                ),
                "email": customer.email or "",
                "phone": customer.latest_phone or "",
                "status": (
                    "active" if customer.is_active else "inactive"
                ),
                "orders_count": customer.orders_count,
                "total_spent": f"{customer.total_spent:.2f}",
                "joined_at": (
                    customer.created_at.isoformat()
                    if customer.created_at else None
                ),
                "last_login": (
                    customer.last_login.isoformat()
                    if customer.last_login else None
                ),
            }
            for customer in customers
        ]