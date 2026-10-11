from datetime import timedelta

from django.utils import timezone
from django.contrib.auth import get_user_model

from accounts.models import LoginHistory

from presence.models import Presence

User = get_user_model()

class UserSummaryService:

    @staticmethod
    def get_summary():

        total_users = User.objects.count()

        active_users = User.objects.filter(
            is_active=True
        ).count()

        today = timezone.localdate()
        now = timezone.now()

        new_today = User.objects.filter(
            created_at__date=today
        ).count()

        new_this_month = User.objects.filter(
            created_at__date__gte=today.replace(day=1)
        ).count()

        buyers = User.objects.filter(
            orders__status="delivered",
            orders__payment__status="paid",
        ).distinct()

        never_purchased = User.objects.exclude(
            id__in=buyers
        )

        buyers_count = buyers.count()
        never_purchased_count = never_purchased.count()

        # Presence

        active_now = Presence.objects.filter(
            last_seen_at__gte=now - timedelta(minutes=3)
        ).count()

        offline_now = Presence.objects.filter(
            last_seen_at__lt=now - timedelta(minutes=3)
        ).count()

        active_today = Presence.objects.filter(
            last_seen_at__date=today
        ).count()

        unique_devices_today = Presence.objects.filter(
            last_seen_at__date=today
        ).values("device_id").distinct().count()

        authenticated_presences = Presence.objects.filter(
            user__isnull=False
        ).count()

        anonymous_presences = Presence.objects.filter(
            user__isnull=True
        ).count()

        try:
            successful_logins_today = LoginHistory.objects.filter(
                logged_in_at__date=today,
                success=True,
            ).count()

            failed_logins_today = LoginHistory.objects.filter(
                logged_in_at__date=today,
                success=False,
            ).count()

        except Exception:
            successful_logins_today = 0
            failed_logins_today = 0

        return {
            "users": {
                "total_users": total_users,
                "active": active_users,
                "new_today": new_today,
                "new_this_month": new_this_month,
            },
            "purchasing": {
                "customers": buyers_count,
                "never_purchased": never_purchased_count,
            },
            "presences": {
                "authenticated": authenticated_presences,
                "anonymous": anonymous_presences,
                "active_now": active_now,
                "offline_now": offline_now,
                "active_today": active_today,
                "unique_devices_today": unique_devices_today,
            },
            "authentication": {
                "successful_logins_today": successful_logins_today,
                "failed_logins_today": failed_logins_today,
            },
        }