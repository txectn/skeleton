from rest_framework.exceptions import Throttled

from .ipThrottle import IPThrottle

class ThrottleService:

    @staticmethod
    def check(
        *,
        request,
        scope,
    ):
        """
        Check whether a request is allowed for the
        given custom throttle scope.

        Raises:
            Throttled: If the rate limit is exceeded.

        Returns:
            True: Request is allowed.
        """

        allowed = IPThrottle.check(
            request=request,
            scope=scope,
        )

        if not allowed:
            raise Throttled(
                detail=(
                    "Too many requests. "
                    "Please try again later."
                )
            )

        return True