from decimal import Decimal

class OrderPriceService:

    @staticmethod
    def calculate(order, shipping):

        subtotal = Decimal("0.00")
        discount = Decimal("0.00")

        # ---------------------------------------------------------
        # Calculate OrderItem prices
        # ---------------------------------------------------------

        for order_item in order.items.all():

            subtotal += order_item.total

            discount += (
                order_item.discount
                * order_item.quantity
            )

        # ---------------------------------------------------------
        # Calculate final Order total
        # ---------------------------------------------------------

        total = subtotal + shipping

        return {
            "subtotal": subtotal,
            "discount": discount,
            "total": total,
        }