from .promotionService import PromotionService

class PromotionResponseService:
    @staticmethod    
    def get_promotion(variant):

        promotion_result = PromotionService.get_variant_promotion(variant)

        promotion = promotion_result["promotion"]
        promotion_variant = promotion_result["promotion_variant"]

        if promotion is None or promotion_variant is None:
            return None

        if promotion.discount_type == "percentage" or promotion.discount_type == "fixed":

            return {
                "id": promotion.id,
                "name": promotion.name,
                "description": promotion.description,
                "discount_type": promotion.discount_type,
                "discount_value": promotion.discount_value,
                "original_price": promotion_result["original_price"],
                "discount_amount": promotion_result["discount_amount"],
                "final_price": promotion_result["final_price"],
                "starts_at": promotion_variant.starts_at,
                "ends_at": promotion_variant.ends_at,
            }

        return None


