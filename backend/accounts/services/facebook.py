import logging

import requests

from django.conf import settings

from rest_framework.exceptions import AuthenticationFailed

logger = logging.getLogger(__name__)

session = requests.Session()


class FacebookService:
    TOKEN_URL = (
        f"https://graph.facebook.com/"
        f"{settings.FACEBOOK_GRAPH_API_VERSION}/oauth/access_token"
    )

    USER_URL = (
        f"https://graph.facebook.com/"
        f"{settings.FACEBOOK_GRAPH_API_VERSION}/me"
    )

    @staticmethod
    def verify(request):
        """
        Verify a Facebook OAuth Authorization Code.

        Flow:
        1. Read the authorization code from the request.
        2. Exchange it for an access token.
        3. Retrieve the Facebook user's profile.
        4. Return a normalized user dictionary.
        """

        authorization = request.headers.get("Authorization")

        if not authorization or not authorization.startswith("Bearer "):
            raise AuthenticationFailed(
                "Facebook authorization code is missing."
            )

        code = authorization.replace("Bearer ", "", 1).strip()

        # ---------------------------------------------------------
        # Exchange authorization code for access token
        # ---------------------------------------------------------

        try:
            token_response = session.get(
                FacebookService.TOKEN_URL,
                params={
                    "client_id": settings.FACEBOOK_APP_ID,
                    "client_secret": settings.FACEBOOK_APP_SECRET,
                    "redirect_uri": settings.FACEBOOK_REDIRECT_URI,
                    "code": code,
                },
                timeout=10,
            )

            token_response.raise_for_status()

        except requests.RequestException:
            logger.exception("Facebook token exchange failed.")
            raise AuthenticationFailed(
                "Unable to authenticate with Facebook."
            )

        try:
            token_data = token_response.json()

        except ValueError:
            logger.exception(
                "Facebook token endpoint returned invalid JSON."
            )
            raise AuthenticationFailed(
                "Unable to authenticate with Facebook."
            )

        access_token = token_data.get("access_token")

        if not access_token:
            logger.error(
                "Facebook token response missing access_token: %s",
                token_data,
            )
            raise AuthenticationFailed(
                "Unable to authenticate with Facebook."
            )

        # ---------------------------------------------------------
        # Retrieve Facebook user
        # ---------------------------------------------------------

        try:
            user_response = session.get(
                FacebookService.USER_URL,
                params={
                    "fields": "id,email,first_name,last_name",
                    "access_token": access_token,
                },
                timeout=10,
            )

            user_response.raise_for_status()

        except requests.RequestException:
            logger.exception("Facebook user request failed.")
            raise AuthenticationFailed(
                "Unable to authenticate with Facebook."
            )

        try:
            user = user_response.json()

        except ValueError:
            logger.exception(
                "Facebook user endpoint returned invalid JSON."
            )
            raise AuthenticationFailed(
                "Unable to authenticate with Facebook."
            )

        provider_user_id = user.get("id")
        email = user.get("email")

        if not provider_user_id:
            logger.error(
                "Facebook response missing user id: %s",
                user,
            )
            raise AuthenticationFailed(
                "Unable to authenticate with Facebook."
            )

        if not email:
            logger.warning(
                "Facebook account %s did not provide an email address.",
                provider_user_id,
            )
            raise AuthenticationFailed(
                "Facebook account does not provide an email address."
            )

        return {
            "provider": "facebook",
            "provider_user_id": provider_user_id,
            "email": email,
            "first_name": user.get("first_name", ""),
            "last_name": user.get("last_name", ""),
        }