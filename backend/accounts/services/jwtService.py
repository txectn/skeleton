from rest_framework_simplejwt.tokens import RefreshToken

class JWTService:
    TOKEN_VERSION_CLAIM = "token_version"

    @staticmethod
    def create_tokens(user) -> dict[str, str]:
        """
        Create JWT access and refresh tokens for the authenticated user.

        The current token version is embedded as a custom claim so it can
        be validated during authentication.

        Returns:
            {
                "access": "<jwt_access_token>",
                "refresh": "<jwt_refresh_token>",
            }
        """

        refresh = RefreshToken.for_user(user)
        refresh[JWTService.TOKEN_VERSION_CLAIM] = user.token_version

        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }