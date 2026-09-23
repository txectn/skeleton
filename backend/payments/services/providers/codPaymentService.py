from rest_framework.exceptions import ValidationError

from payments.models import Payment

class CodPaymentService:

    @staticmethod
    def process(order):

        payment = Payment.objects.filter(
            order=order,
        ).first()

        if payment and payment.status == Payment.Status.PAID:
            raise ValidationError(
                {
                    "payment": (
                        "This order has already been paid."
                    )
                }
            )

        if payment:
            payment.method = Payment.Method.COD
            payment.status = Payment.Status.PENDING
            payment.save(
                update_fields=[
                    "method",
                    "status",
                    "updated_at",
                ]
            )
        else:
            payment = Payment.objects.create(
                order=order,
                method=Payment.Method.COD,
                status=Payment.Status.PENDING,
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
            "payment_method": payment.method,
            "payment_status": payment.status,
            "order_id": order.id,
            "order_status": order.status,
        }