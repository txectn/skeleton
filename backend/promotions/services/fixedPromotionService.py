from decimal import Decimal, ROUND_HALF_UP

from .promotionPriceValidationService import (
    PromotionPriceValidationService,
)

class FixedPromotionService:

    MONEY_QUANT = Decimal("0.01")

    @staticmethod
    def calculate(variant, promotion):

        original_price = Decimal(variant.price)

        discount_value = (
            PromotionPriceValidationService.validate_discount_value(
                promotion.discount_value
            )
        )

        if discount_value is None:
            return None

        # Discount cannot exceed the original price.
        discount_amount = min(
            discount_value,
            original_price,
        )

        final_price = original_price - discount_amount

        final_price = (
            PromotionPriceValidationService.validate_final_price(
                final_price,
                variant.cost_price,
            )
        )

        if final_price is None:
            return None

        discount_amount = discount_amount.quantize(
            FixedPromotionService.MONEY_QUANT,
            rounding=ROUND_HALF_UP,
        )

        final_price = final_price.quantize(
            FixedPromotionService.MONEY_QUANT,
            rounding=ROUND_HALF_UP,
        )

        return {
            "original_price": original_price,
            "discount_amount": discount_amount,
            "final_price": final_price,
            "promotion": promotion,
        }
