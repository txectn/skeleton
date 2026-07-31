# from django.conf import settings
# from clerk_backend_api import Clerk

# class ClerkVerificationService:
#     @staticmethod
#     def verify(token):
#         clerk = Clerk(bearer_auth=settings.CLERK_SECRET_KEY)

#         try:
#             clerk.verify_token(token)

#             print("Token verified: True")
#             return True

#         except Exception:
#             print("Token verified: False")
#             return False












# from django.conf import settings
# from clerk_backend_api import Clerk


# class ClerkVerificationService:
#     @staticmethod
#     def verify(request):
#         secret_key = getattr(settings, "CLERK_SECRET_KEY", None)

#         if secret_key:
#             print("Clerk secret key: Loaded")
#         else:
#             print("Clerk secret key: Missing")

#         clerk = Clerk(bearer_auth=secret_key)

#         try:
#             clerk.verify_token(token)

#             print("Token verified: True")
#             return True

#         except Exception as e:
#             print("Token verified: False")
#             print(f"Error: {e}")
#             return False

















# from django.conf import settings

# from clerk_backend_api import Clerk
# from clerk_backend_api.security.types import AuthenticateRequestOptions


# class ClerkVerificationService:
#     @staticmethod
#     def verify(request):
#         secret_key = getattr(settings, "CLERK_SECRET_KEY", None)
        
#         authorized_parties = getattr(settings, "CSRF_TRUSTED_ORIGINS", [])

#         if secret_key:
#             print("Clerk secret key: Loaded")
#         else:
#             print("Clerk secret key: Missing")
#             return False

#         clerk = Clerk(bearer_auth=secret_key)

#         try:
#             request_state = clerk.authenticate_request(
#                 request,
#                 AuthenticateRequestOptions(
#                     authorized_parties=authorized_parties,
#                 ),
#             )

#             print(f"Token verified: {request_state.is_signed_in}")

#             return request_state.is_signed_in

#         except Exception as e:
#             print("Token verified: False")
#             print(f"Error: {e}")
#             return False




















# from django.conf import settings

# from clerk_backend_api import Clerk
# from clerk_backend_api.security.types import AuthenticateRequestOptions

# from rest_framework.exceptions import AuthenticationFailed, APIException


# class ClerkVerificationService:
#     @staticmethod
#     def verify(request):
#         """
#         Verify the Clerk session from the Authorization header.

#         Returns:
#             Clerk user object

#         Raises:
#             AuthenticationFailed: If authentication fails.
#             APIException: If the authentication service is misconfigured or unavailable.
#         """

#         secret_key = getattr(settings, "CLERK_SECRET_KEY", None)
#         if not secret_key:
#             raise APIException("Clerk secret key is not configured.")

#         authorized_parties = getattr(settings, "CSRF_TRUSTED_ORIGINS", [])

#         clerk = Clerk(bearer_auth=secret_key)

#         try:
#             request_state = clerk.authenticate_request(
#                 request,
#                 AuthenticateRequestOptions(
#                     authorized_parties=authorized_parties,
#                 ),
#             )

#         except Exception as exc:
#             # Clerk SDK/network/internal error
#             raise APIException("Failed to verify Clerk token.") from exc

#         if not request_state.is_signed_in:
#             raise AuthenticationFailed("Invalid or expired authentication token.")

#         if request_state.payload is None:
#             raise AuthenticationFailed("Authentication token payload is missing.")

#         return request_state.payload















# from django.conf import settings

# from clerk_backend_api import Clerk
# from clerk_backend_api.security.types import AuthenticateRequestOptions

# from rest_framework.exceptions import AuthenticationFailed, APIException


# class ClerkVerificationService:
#     @staticmethod
#     def verify(request):
#         """
#         Verify the Clerk session and return the authenticated email.

#         Returns:
#             {
#                 "email": "user@example.com"
#             }

#         Raises:
#             AuthenticationFailed
#             APIException
#         """

#         secret_key = getattr(settings, "CLERK_SECRET_KEY", None)
#         if not secret_key:
#             raise APIException("Clerk secret key is not configured.")

#         authorized_parties = getattr(settings, "CSRF_TRUSTED_ORIGINS", [])

#         with Clerk(bearer_auth=secret_key) as clerk:

#             # Verify session token
#             try:
#                 request_state = clerk.authenticate_request(
#                     request,
#                     AuthenticateRequestOptions(
#                         authorized_parties=authorized_parties,
#                     ),
#                 )
#             except Exception as exc:
#                 raise APIException("Failed to verify Clerk token.") from exc

#             if not request_state.is_signed_in:
#                 reason = getattr(request_state, "reason", None)
#                 raise AuthenticationFailed(
#                     reason or "Invalid or expired authentication token."
#                 )

#             payload = request_state.payload
#             if not payload:
#                 raise AuthenticationFailed(
#                     "Authentication token payload is missing."
#                 )

#             clerk_user_id = payload.get("sub")
#             if not clerk_user_id:
#                 raise AuthenticationFailed(
#                     "User ID is missing from authentication token."
#                 )

#             # Fetch Clerk user
#             try:
#                 clerk_user = clerk.users.get(user_id=clerk_user_id)
#             except Exception as exc:
#                 raise APIException("No User found.") from exc

#         # Find the primary email
#         primary_email = None

#         for email in clerk_user.email_addresses:
#             if email.id == clerk_user.primary_email_address_id:
#                 primary_email = email.email_address
#                 break

#         if primary_email is None:
#             raise AuthenticationFailed(
#                 "Primary email address not found."
#             )

#         return {
#             "email": primary_email,
#         }



















# from django.conf import settings

# from clerk_backend_api import Clerk
# from clerk_backend_api.security.types import AuthenticateRequestOptions

# from rest_framework.exceptions import AuthenticationFailed, APIException


# class ClerkVerificationService:
#     @staticmethod
#     def verify(request):
#         """
#         Verify the Clerk session and return the authenticated user's email.

#         Returns:
#             {
#                 "email": "user@example.com"
#             }

#         Raises:
#             AuthenticationFailed:
#                 Authentication could not be verified.

#             APIException:
#                 Authentication service is unavailable.
#         """

#         secret_key = getattr(settings, "CLERK_SECRET_KEY", None)
#         if not secret_key:
#             raise APIException("Authentication service is unavailable.")

#         authorized_parties = getattr(settings, "CSRF_TRUSTED_ORIGINS", [])

#         with Clerk(bearer_auth=secret_key) as clerk:

#             # Verify the Clerk session.
#             try:
#                 request_state = clerk.authenticate_request(
#                     request,
#                     AuthenticateRequestOptions(
#                         authorized_parties=authorized_parties,
#                     ),
#                 )
#             except Exception as exc:
#                 raise APIException("Authentication service is unavailable.") from exc

#             if not request_state.is_signed_in:
#                 raise AuthenticationFailed("Authentication failed.")

#             payload = request_state.payload
#             if not payload:
#                 raise AuthenticationFailed("Authentication failed.")

#             clerk_user_id = payload.get("sub")
#             if not clerk_user_id:
#                 raise AuthenticationFailed("Authentication failed.")

#             # Fetch the authenticated Clerk user.
#             try:
#                 clerk_user = clerk.users.get(user_id=clerk_user_id)
#             except Exception as exc:
#                 raise AuthenticationFailed("Authentication failed.") from exc

#         # Find the primary email address.
#         primary_email = next(
#             (
#                 email.email_address
#                 for email in clerk_user.email_addresses
#                 if email.id == clerk_user.primary_email_address_id
#             ),
#             None,
#         )

#         if primary_email is None:
#             raise AuthenticationFailed("Authentication failed.")

#         return {
#             "email": primary_email,
#         }





















import logging

from django.conf import settings

from clerk_backend_api import Clerk
from clerk_backend_api.security.types import AuthenticateRequestOptions

from rest_framework.exceptions import AuthenticationFailed, APIException

logger = logging.getLogger(__name__)


class ClerkVerificationService:
    @staticmethod
    def verify(request):
        """
        Verify the Clerk session and return the authenticated user's email.

        Returns:
            {
                "email": "user@example.com",
            }

        Raises:
            AuthenticationFailed:
                Authentication failed.

            APIException:
                Authentication service is unavailable.
        """

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
            "email": primary_email,
        }