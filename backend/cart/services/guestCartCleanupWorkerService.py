from datetime import timedelta

from django.db.models import Max, Q
from django.utils import timezone

from ..models import Cart

class GuestCartCleanupWorkerService:

    INACTIVE_DAYS = 3

    @staticmethod
    def cleanup():
        cutoff = timezone.now() - timedelta(
            days=GuestCartCleanupWorkerService.INACTIVE_DAYS,
        )

        guest_carts = (
            Cart.objects
            .filter(
                user__isnull=True,
            )
            .annotate(
                last_item_updated_at=Max(
                    "items__updated_at",
                ),
            )
            .filter(
                Q(
                    last_item_updated_at__lt=cutoff,
                )
                |
                Q(
                    last_item_updated_at__isnull=True,
                    updated_at__lt=cutoff,
                )
            )
        )

        deleted_count, _ = guest_carts.delete()

        return deleted_count