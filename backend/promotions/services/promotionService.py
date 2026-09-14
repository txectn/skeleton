from decimal import Decimal

from ..models import Promotion

from .promotionSelectionService import PromotionSelectionService
from .percentagePromotionService import PercentagePromotionService
from .fixedPromotionService import FixedPromotionService

class PromotionService:

    @staticmethod
    def get_variant_promotion(variant):

        promotion_variant = (
            PromotionSelectionService.get_promotion(variant)
        )

        if promotion_variant is None:
            return {
                "original_price": variant.price,
                "discount_amount": Decimal("0.00"),
                "final_price": variant.price,
                "promotion": None,
                "promotion_variant": None,
            }

        promotion = promotion_variant.promotion

        if promotion.discount_type == Promotion.DiscountType.PERCENTAGE:

            final_promotion = PercentagePromotionService.calculate(
                variant,
                promotion,
            )

        elif promotion.discount_type == Promotion.DiscountType.FIXED:

            final_promotion = FixedPromotionService.calculate(
                variant,
                promotion,
            )

        else:
            raise ValueError(
                f"Unsupported promotion discount type: "
                f"{promotion.discount_type}"
            )

        if final_promotion is None:
            return {
                "original_price": variant.price,
                "discount_amount": Decimal("0.00"),
                "final_price": variant.price,
                "promotion": None,
                "promotion_variant": None,
            }

        final_promotion["promotion_variant"] = promotion_variant

        return final_promotion




