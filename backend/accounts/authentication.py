from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication

class VersionedJWTAuthentication(JWTAuthentication):
    """
    JWT authentication with token-version validation.

    A token is accepted only when its token_version claim matches
    the user's current token_version in the database.

    Incrementing user.token_version therefore invalidates all
    previously issued tokens for that user.
    """

    TOKEN_VERSION_CLAIM = "token_version"

    def get_user(self, validated_token):
        user = super().get_user(validated_token)

        token_version = validated_token.get(self.TOKEN_VERSION_CLAIM)

        if token_version is None:
            raise AuthenticationFailed(
                "Invalid authentication credentials.",
                code="authentication_failed",
            )

        if token_version != user.token_version:
            raise AuthenticationFailed(
                "Invalid authentication credentials.",
                code="authentication_failed",
            )

        return user