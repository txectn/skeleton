import logging

from django.conf import settings

from clerk_backend_api import Clerk
from clerk_backend_api.security.types import AuthenticateRequestOptions

from rest_framework.exceptions import AuthenticationFailed, APIException

logger = logging.getLogger(__name__)

class ClerkVerificationService:
    @staticmethod
    def verify(request):
        secret_key = getattr(settings, "CLERK_SECRET_KEY", None)
        if not secret_key:
            logger.error("CLERK_SECRET_KEY is not configured.")
            raise APIException("Authentication service is unavailable.")

        authorized_parties = getattr(settings, "CLERK_AUTHORIZED_PARTIES", [])

        try:
            with Clerk(bearer_auth=secret_key) as clerk:

                request_state = clerk.authenticate_request(
                    request,
                    AuthenticateRequestOptions(
                        authorized_parties=authorized_parties,
                    ),
                )

                if not request_state.is_signed_in:
                    raise AuthenticationFailed("Authentication failed.")

                payload = request_state.payload
                if not payload:
                    raise AuthenticationFailed("Authentication failed.")

                clerk_user_id = payload.get("sub")
                if not clerk_user_id:
                    raise AuthenticationFailed("Authentication failed.")

                clerk_user = clerk.users.get(user_id=clerk_user_id)

        except AuthenticationFailed:
            raise

        except Exception as exc:
            logger.exception("Clerk authentication failed.")
            raise APIException("Authentication service is unavailable.") from exc

        primary_email = next(
            (
                email.email_address
                for email in clerk_user.email_addresses
                if email.id == clerk_user.primary_email_address_id
            ),
            None,
        )

        if not primary_email:
            logger.error(
                "Primary email not found for Clerk user '%s'.",
                clerk_user_id,
            )
            raise AuthenticationFailed("Authentication failed.")

        return {
            "provider": "clerk",
            "email": primary_email,
            "provider_user_id": clerk_user_id,
            "first_name": clerk_user.first_name,
            "last_name": clerk_user.last_name,
        }