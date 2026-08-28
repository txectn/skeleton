import logging

import requests

from django.conf import settings

from google.auth.transport import requests as google_requests
from google.oauth2 import id_token

from rest_framework.exceptions import (
    APIException,
    AuthenticationFailed,
)

logger = logging.getLogger(__name__)


class GoogleService:
    TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"
    TIMEOUT = 10

    @staticmethod
    def verify(request):
        client_id = getattr(settings, "GOOGLE_CLIENT_ID", None)
        client_secret = getattr(settings, "GOOGLE_CLIENT_SECRET", None)
        redirect_uri = getattr(settings, "GOOGLE_REDIRECT_URI", None)

        if not all((client_id, client_secret, redirect_uri)):
            logger.error("Google OAuth configuration is incomplete.")
            raise APIException(
                "Authentication service is unavailable."
            )

        auth_header = request.headers.get("Authorization", "")

        if not auth_header.startswith("Bearer "):
            raise AuthenticationFailed("Authentication failed.")

        authorization_code = auth_header.removeprefix("Bearer ").strip()

        if not authorization_code:
            raise AuthenticationFailed("Authentication failed.")

        try:
            response = requests.post(
                GoogleService.TOKEN_ENDPOINT,
                data={
                    "code": authorization_code,
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "redirect_uri": redirect_uri,
                    "grant_type": "authorization_code",
                },
                timeout=GoogleService.TIMEOUT,
            )

            response.raise_for_status()

            token_data = response.json()

            google_id_token = token_data.get("id_token")

            if not google_id_token:
                logger.warning(
                    "Google token response missing id_token."
                )
                raise AuthenticationFailed(
                    "Authentication failed."
                )

            payload = id_token.verify_oauth2_token(
                google_id_token,
                google_requests.Request(),
                client_id,
            )

        except requests.HTTPError:
            logger.warning(
                "Google rejected authorization code."
            )
            raise AuthenticationFailed(
                "Authentication failed."
            )

        except requests.RequestException:
            logger.exception(
                "Failed to communicate with Google."
            )
            raise APIException(
                "Authentication service is unavailable."
            )

        except ValueError:
            logger.warning(
                "Google returned an invalid ID token."
            )
            raise AuthenticationFailed(
                "Authentication failed."
            )

        except Exception:
            logger.exception(
                "Unexpected Google authentication error."
            )
            raise APIException(
                "Authentication service is unavailable."
            )

        if not payload.get("email_verified"):
            raise AuthenticationFailed(
                "Authentication failed."
            )

        email = payload.get("email")
        provider_user_id = payload.get("sub")

        if not email or not provider_user_id:
            raise AuthenticationFailed(
                "Authentication failed."
            )

        return {
            "provider": "google",
            "email": email,
            "provider_user_id": provider_user_id,
            "first_name": payload.get("given_name"),
            "last_name": payload.get("family_name"),
        }