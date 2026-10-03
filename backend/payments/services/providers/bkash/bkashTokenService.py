import logging

import requests

from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)

class BkashTokenService:
    """Manages the bKash token lifecycle and Redis caching."""

    ID_TOKEN_KEY = "bkash_id_token"
    REFRESH_TOKEN_KEY = "bkash_refresh_token"

    @classmethod
    def _get_auth_headers(cls) -> dict:

        """Build headers required by bKash token endpoints."""

        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "username": settings.BKASH_USERNAME,
            "password": settings.BKASH_PASSWORD,
        }

    @classmethod
    def get_id_token(cls) -> str:

        """
        Returns a valid id_token.

        Uses the cached token first, then attempts a refresh,
        and finally requests a new grant token if necessary.
        """
        
        id_token = cache.get(cls.ID_TOKEN_KEY)

        if id_token:
            return id_token

        refresh_token = cache.get(cls.REFRESH_TOKEN_KEY)

        if refresh_token:
            logger.info(
                "bKash id_token expired. Attempting token refresh..."
            )

            try:
                return cls.refresh_token(refresh_token)
            
            except Exception as exc:
                logger.warning(
                    "bKash token refresh failed: %s. "
                    "Falling back to grant token.",
                    exc,
                )

        logger.info("Requesting new bKash Grant Token...")

        return cls.grant_token()

    @classmethod
    def grant_token(cls) -> str:

        """Request and cache a new bKash token pair."""
        
        url = (
            f"{settings.BKASH_BASE_URL}"
            "/v2/tokenized-checkout/auth/grant-token"
        )

        payload = {
            "app_key": settings.BKASH_APP_KEY,
            "app_secret": settings.BKASH_APP_SECRET,
        }

        try:
            response = requests.post(
                url,
                json=payload,
                headers=cls._get_auth_headers(),
                timeout=10,
            )
            data = response.json()

        except requests.RequestException as exc:
            logger.error(
                "Network error during bKash grant token call: %s",
                exc,
            )
            raise Exception("bKash server unreachable.") from exc

        if (
            response.status_code == 200
            and data.get("statusCode") == "0000"
        ):
            id_token = data.get("id_token")
            refresh_token = data.get("refresh_token")

            cache.set(
                cls.ID_TOKEN_KEY,
                id_token,
                timeout=55 * 60,
            )

            cache.set(
                cls.REFRESH_TOKEN_KEY,
                refresh_token,
                timeout=27 * 24 * 60 * 60,
            )

            return id_token

        error_message = data.get(
            "statusMessage",
            "Unknown Error",
        )

        logger.error(
            "Failed to grant bKash token: %s",
            data,
        )

        raise Exception(
            f"bKash Grant Token Error: {error_message}"
        )

    @classmethod
    def refresh_token(cls, refresh_token: str) -> str:

        """Refresh the bKash id_token and update the cached tokens."""

        url = (
            f"{settings.BKASH_BASE_URL}"
            "/v2/tokenized-checkout/auth/refresh-token"
        )

        payload = {
            "app_key": settings.BKASH_APP_KEY,
            "app_secret": settings.BKASH_APP_SECRET,
            "refresh_token": refresh_token,
        }

        try:
            response = requests.post(
                url,
                json=payload,
                headers=cls._get_auth_headers(),
                timeout=10,
            )
            data = response.json()

        except requests.RequestException as exc:
            logger.error(
                "Network error during bKash refresh token call: %s",
                exc,
            )
            return cls.grant_token()

        if (
            response.status_code == 200
            and data.get("statusCode") == "0000"
        ):
            id_token = data.get("id_token")
            new_refresh_token = data.get("refresh_token")

            cache.set(
                cls.ID_TOKEN_KEY,
                id_token,
                timeout=55 * 60,
            )

            cache.set(
                cls.REFRESH_TOKEN_KEY,
                new_refresh_token,
                timeout=27 * 24 * 60 * 60,
            )

            return id_token

        logger.warning(
            "bKash refresh token failed (%s). "
            "Requesting a new Grant Token...",
            data.get("statusMessage"),
        )

        return cls.grant_token()



'''
# use -> 

id_token = BkashTokenService.get_id_token()

'''