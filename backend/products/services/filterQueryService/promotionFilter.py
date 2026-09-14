from django.db.models import Q
from django.utils import timezone

from .base import BaseFilter

class PromotionFilter(BaseFilter):
    PARAM_NAME = "has_promotion"

    def apply(self, queryset, params):
        has_promotion = params.get(self.PARAM_NAME)

        if has_promotion is None:
            return queryset

        if has_promotion not in ("true", "false"):
            return queryset

        now = timezone.now()

        valid_promotion = Q(
            variants__is_active=True,
            variants__promotion_variants__promotion__is_active=True,
            variants__promotion_variants__starts_at__lte=now,
            variants__promotion_variants__ends_at__gt=now,
        )

        if has_promotion == "true":
            return queryset.filter(
                valid_promotion
            ).distinct()

        return queryset.exclude(
            valid_promotion
        ).distinct()