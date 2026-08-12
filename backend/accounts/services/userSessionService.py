import hashlib

from django.utils import timezone

from rest_framework_simplejwt.settings import api_settings

from ..models import UserSession

class UserSessionService:
    @staticmethod
    def create(
        *,
        user,
        refresh_token,
        ip_address,
        device,
    ):
        """
        Create a new authenticated user session.
        """

        refresh_token_hash = hashlib.sha256(
            refresh_token.encode("utf-8")
        ).hexdigest()

        return UserSession.objects.create(
            user=user,
            refresh_token_hash=refresh_token_hash,
            device=device.get("device", ""),
            browser=device.get("browser", ""),
            operating_system=device.get(
                "operating_system",
                "",
            ),
            ip_address=ip_address,
            expires_at=(
                timezone.now()
                + api_settings.REFRESH_TOKEN_LIFETIME
            ),
            last_activity=timezone.now(),
            is_active=True,
        )