from django.db.models import Q
from django.utils import timezone

from .base import BaseFilter

class PromotionIdFilter(BaseFilter):
    PARAM_NAME = "promotion"

    def apply(self, queryset, params):
        promotion_id = params.get(self.PARAM_NAME)

        if not promotion_id:
            return queryset

        now = timezone.now()

        valid_promotion = Q(
            variants__is_active=True,
            variants__promotion_variants__promotion_id=promotion_id,
            variants__promotion_variants__promotion__is_active=True,
            variants__promotion_variants__starts_at__lte=now,
            variants__promotion_variants__ends_at__gt=now,
        )

        return queryset.filter(
            valid_promotion
        ).distinct()