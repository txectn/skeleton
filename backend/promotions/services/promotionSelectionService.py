# from django.utils import timezone

# # from ..models import PromotionVariant

# class PromotionSelectionService:

#     @staticmethod
#     def get_promotion(variant, PromotionVariant):

#         now = timezone.now()

#         return (
#             PromotionVariant.objects
#             .select_related("promotion")
#             .filter(
#                 variant=variant,
#                 promotion__is_active=True,
#                 starts_at__lte=now,
#                 ends_at__gt=now,
#             )
#             .order_by(
#                 "-promotion__priority",
#                 "-promotion__created_at",
#             )
#             .first()
#         )

from django.utils import timezone

from ..models import PromotionVariant

class PromotionSelectionService:

    @staticmethod
    def get_promotion(variant):

        now = timezone.now()

        promotion_variant = (
            PromotionVariant.objects
            .select_related("promotion")
            .filter(
                variant=variant,
                promotion__is_active=True,
                starts_at__lte=now,
                ends_at__gt=now,
            )
            .order_by(
                "-promotion__priority",
                "-promotion__created_at",
            )
            .first()
        )

        if promotion_variant is None:
            return None

        return promotion_variant