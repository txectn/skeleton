from django.conf import settings
from django.core.cache import cache

from ipware import get_client_ip

class IPThrottle:

    @staticmethod
    def check(
        *,
        request,
        scope,
    ):
        """
        Check whether the client IP is allowed to perform
        an action within the configured rate limit.

        Returns:
            True  -> request is allowed
            False -> rate limit exceeded
        """

        # ---------------------------------------------------------
        # Get configured rate
        # ---------------------------------------------------------

        rate = settings.CUSTOM_THROTTLE_RATES.get(
            scope,
        )

        if not rate:
            raise ValueError(
                f"Throttle scope '{scope}' is not configured."
            )

        # ---------------------------------------------------------
        # Get client IP
        # ---------------------------------------------------------

        client_ip, _ = get_client_ip(request)

        if not client_ip:
            raise ValueError(
                "Unable to determine client IP address."
            )

        # ---------------------------------------------------------
        # Parse rate
        # ---------------------------------------------------------

        num_requests, period = rate.split("/")

        num_requests = int(num_requests)

        period_seconds = {
            "sec": 1,
            "min": 60,
            "hour": 3600,
            "day": 86400,
        }.get(period)

        if period_seconds is None:
            raise ValueError(
                f"Unsupported throttle period: {period}"
            )

        # ---------------------------------------------------------
        # Cache key
        # ---------------------------------------------------------

        cache_key = (
            f"custom_throttle:"
            f"{scope}:"
            f"{client_ip}"
        )

        # ---------------------------------------------------------
        # Get current request count
        # ---------------------------------------------------------

        current_count = cache.get(
            cache_key,
            0,
        )

        # ---------------------------------------------------------
        # Check limit
        # ---------------------------------------------------------

        if current_count >= num_requests:
            return False

        # ---------------------------------------------------------
        # Increase request count
        # ---------------------------------------------------------

        if current_count == 0:

            cache.set(
                cache_key,
                1,
                timeout=period_seconds,
            )

        else:

            cache.incr(
                cache_key,
            )

        return True



'''
IPThrottle.check(
    request=request,
    scope="guest_cart_creation",
)
'''