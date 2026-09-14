from decimal import Decimal

class PromotionPriceValidationService:

    @staticmethod
    def validate_discount_value(discount_value):
        discount_value = Decimal(discount_value)

        if discount_value < 0:
            return None

        return discount_value

    @staticmethod
    def validate_percentage(discount_value):
        discount_value = Decimal(discount_value)

        if discount_value > Decimal("100"):
            return None

        return discount_value

    @staticmethod
    def validate_final_price(final_price, cost_price):
        if cost_price is None:
            return final_price

        cost_price = Decimal(cost_price)
        final_price = Decimal(final_price)

        if final_price < cost_price:
            return None

        return final_price