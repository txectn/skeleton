from django.db import transaction

from ..models import Profile

class ProfileService:
    @staticmethod
    @transaction.atomic
    def get_or_create(user):
        """
        Get the user's profile or create one if it does not exist.

        This method is idempotent and safe to call on every login.
        """

        profile, _ = Profile.objects.get_or_create(
            user=user,
        )

        return profile