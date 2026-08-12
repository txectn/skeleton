import hashlib

from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from ..models import UserSession
from .jwtService import JWTService

class RefreshTokenService:
    """
    Validates a refresh token against the JWT, user, and server-side session,
    then generates a new access token.
    """

    @staticmethod
    def refresh(refresh_token: str) -> dict[str, str]:
        if not refresh_token:
            raise AuthenticationFailed(
                "Invalid authentication credentials.",
                code="authentication_failed",
            )

        # Validate JWT signature, token type, and expiration.
        try:
            refresh = RefreshToken(refresh_token)
        except TokenError:
            raise AuthenticationFailed(
                "Invalid authentication credentials.",
                code="authentication_failed",
            )

        user_id = refresh.get("user_id")
        token_version = refresh.get(
            JWTService.TOKEN_VERSION_CLAIM
        )

        if user_id is None or token_version is None:
            raise AuthenticationFailed(
                "Invalid authentication credentials.",
                code="authentication_failed",
            )

        # Match the refresh token against a server-side session.
        refresh_token_hash = hashlib.sha256(
            refresh_token.encode("utf-8")
        ).hexdigest()

        try:
            session = (
                UserSession.objects
                .select_related("user")
                .get(
                    user_id=user_id,
                    refresh_token_hash=refresh_token_hash,
                )
            )
        except UserSession.DoesNotExist:
            raise AuthenticationFailed(
                "Invalid authentication credentials.",
                code="authentication_failed",
            )

        user = session.user

        # Do not issue tokens for inactive users.
        if not user.is_active:
            raise AuthenticationFailed(
                "Invalid authentication credentials.",
                code="authentication_failed",
            )

        # Global session invalidation.
        if token_version != user.token_version:
            raise AuthenticationFailed(
                "Invalid authentication credentials.",
                code="authentication_failed",
            )

        # Issue a new access token while keeping the refresh token.
        access_token = refresh.access_token

        return {
            "access": str(access_token),
        }