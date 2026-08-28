import logging
import secrets

from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction

from rest_framework.exceptions import AuthenticationFailed

logger = logging.getLogger(__name__)

User = get_user_model()

class UserService:

    """
    email = provider_user["email"]
    provider_user_id = provider_user["provider_user_id"]
    first_name = provider_user["first_name"]
    last_name = provider_user["last_name"]

    if email:
        user = find_user_by_email(email)
        if user:
            return user

        return create_user(email, first_name, last_name, provider_user_id)

    user = find_user_by_provider_user_id(provider_user_id)
    if user:
        return user

    return create_user(email, first_name, last_name, provider_user_id)
    """

    @staticmethod
    @transaction.atomic
    def get_or_create(provider_user):
        """
        Get existing user or create a new one.

        provider_user example:

        {
            "provider": "google",
            "email": "user@gmail.com",
            "provider_user_id": "123456",
            "first_name": "John",
            "last_name": "Doe"
        }

        Stored provider_user_id:

        google_123456
        facebook_123456
        clerk_123456
        """

        email = provider_user.get("email")

        provider = provider_user.get(
            "provider"
        )

        raw_provider_user_id = provider_user.get(
            "provider_user_id"
        )

        # ---------------------------------------------------------
        # Validate OAuth data internally
        # ---------------------------------------------------------

        if not provider or not raw_provider_user_id:

            logger.error(
                "OAuth provider data is incomplete."
            )

            raise AuthenticationFailed(
                "Authentication failed."
            )

        provider_user_id = (
            f"{provider}_{raw_provider_user_id}"
        )

        first_name = (
            provider_user.get("first_name")
            or ""
        )

        last_name = (
            provider_user.get("last_name")
            or ""
        )

        # ---------------------------------------------------------
        # Find existing user
        # ---------------------------------------------------------

        user = None

        try:

            if email:

                user = User.objects.get(
                    email=email
                )

            else:

                user = User.objects.get(
                    provider_user_id=provider_user_id
                )

        except User.DoesNotExist:
            pass

        # ---------------------------------------------------------
        # Existing user update
        # ---------------------------------------------------------

        if user:

            update_fields = []

            # Only set first_name if user doesn't already have one
            if (
                first_name
                and not user.first_name
            ):

                user.first_name = first_name

                update_fields.append(
                    "first_name"
                )

            # Only set last_name if user doesn't already have one
            if (
                last_name
                and not user.last_name
            ):

                user.last_name = last_name

                update_fields.append(
                    "last_name"
                )

            if (
                not user.provider_user_id
                or user.provider_user_id != provider_user_id
            ):

                user.provider_user_id = provider_user_id

                update_fields.append(
                    "provider_user_id"
                )

            if update_fields:

                user.save(
                    update_fields=update_fields
                )

                logger.info(
                    "Updated OAuth user data. email=%s",
                    email,
                )

            return user

        # ---------------------------------------------------------
        # Create new user
        # ---------------------------------------------------------

        try:

            user = UserService.create(
                email=email,
                first_name=first_name,
                last_name=last_name,
                provider_user_id=provider_user_id,
            )

            logger.info(
                "Created OAuth user. email=%s provider_user_id=%s",
                email,
                provider_user_id,
            )

            return user

        except IntegrityError:

            logger.warning(
                "User creation race condition detected. email=%s",
                email,
            )

            try:

                if email:

                    return User.objects.get(
                        email=email
                    )

                return User.objects.get(
                    provider_user_id=provider_user_id
                )

            except User.DoesNotExist:

                logger.exception(
                    "User creation failed after IntegrityError."
                )

                raise AuthenticationFailed(
                    "Authentication failed."
                )

    @staticmethod
    def create(
        *,
        email,
        first_name,
        last_name,
        provider_user_id,
    ):
        """
        Create a new user.
        """

        return User.objects.create(
            username=UserService.generate_username(),
            email=email,
            first_name=first_name,
            last_name=last_name,
            provider_user_id=provider_user_id,
            is_verified=True,
        )

    @staticmethod
    def generate_username():
        """
        Generate a unique random username.
        """

        while True:

            username = secrets.token_urlsafe(12)

            if not User.objects.filter(
                username=username
            ).exists():

                return username
            






