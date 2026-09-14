from django.contrib.auth import get_user_model

from ..models import LoginHistory

class LoginHistoryService:
    @staticmethod
    def create(
        *,
        user_id,
        provider,
        provider_user,
        device,
        ip_address,
        success,
    ):
        """
        Create a login history record.

        Args:
            user_id: Local user ID.
            provider: Authentication provider.
            provider_user: Verified user data returned by the provider.
            device: Device information from the client.
            ip_address: Client IP address.
            success: Whether the authentication attempt succeeded.
        """

        # Get the user instance
        user = get_user_model().objects.filter(id=user_id).first()

        provider_user = provider_user or {}
        device = device or {}

        return LoginHistory.objects.create(
            user=user,
            provider=provider,
            email=provider_user.get("email"),
            ip_address=ip_address,
            device=device.get("device", ""),
            browser=device.get("browser", ""),
            operating_system=device.get("operating_system", ""),
            success=success,
        )