import logging

from ipware import get_client_ip

from rest_framework.exceptions import ValidationError

from .clerk_verification import ClerkVerificationService
from .google import GoogleService
from .facebook import FacebookService

from .userService import UserService
from .profileService import ProfileService
from .jwtService import JWTService
from .userSessionService import UserSessionService
from .loginHistoryService import LoginHistoryService

logger = logging.getLogger(__name__)

class AuthService:
    @staticmethod
    def login(request, provider, device):
        """
        Authentication Flow

        1. Determine the authentication provider.
        2. Verify the provider token.
        3. Get or create the local user.
        4. Get or create the user profile.
        5. Generate JWT tokens.
        6. Store the refresh token in the user session.
        7. Record login history.
        8. Return the JWT tokens.
        """

        ip_address, _ = get_client_ip(request)

        user = None
        provider_user = None
        tokens = None

        try:
            # ---------------------------------------------------------
            # Verify provider
            # ---------------------------------------------------------

            if provider == "clerk":
                provider_user = ClerkVerificationService.verify(request)

            elif provider == "google":
                provider_user = GoogleService.verify(request)

            elif provider == "facebook":
                provider_user = FacebookService.verify(request)

            else:
                raise ValidationError("Authentication failed.")

            # ---------------------------------------------------------
            # User
            # ---------------------------------------------------------

            user = UserService.get_or_create(provider_user)

            # ---------------------------------------------------------
            # Profile
            # ---------------------------------------------------------

            ProfileService.get_or_create(user)

            # ---------------------------------------------------------
            # JWT
            # ---------------------------------------------------------

            tokens = JWTService.create_tokens(user)

            # ---------------------------------------------------------
            # User session
            # ---------------------------------------------------------

            UserSessionService.create(
                user=user,
                refresh_token=tokens["refresh"],
                ip_address=ip_address,
                device=device,
            )

            return {
                "tokens": tokens,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
            }

        finally:
            try:
                LoginHistoryService.create(
                    user=user,
                    provider=provider,
                    provider_user=provider_user,
                    device=device,
                    ip_address=ip_address,
                    success=user is not None,
                )
                
            except Exception:
                logger.exception(
                    "Failed to create login history."
                )





