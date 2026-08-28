from django.conf import settings
from django.core.cache import cache

class CaptchaRate:

    RATE_PREFIX = "captcha_rate"

    PERIODS = {
        "second": 1,
        "sec": 1,
        "s": 1,

        "minute": 60,
        "min": 60,
        "m": 60,

        "hour": 3600,
        "h": 3600,

        "day": 86400,
        "d": 86400,
    }

    def __init__(self, scope):
        self.scope = scope

        self.rate = settings.CAPTCHA_RATES.get(
            scope
        )

        if not self.rate:
            raise ValueError(
                f"CAPTCHA rate is not configured "
                f"for scope '{scope}'."
            )

        self.max_requests, self.time_range = (
            self._parse_rate()
        )

    def _parse_rate(self):
        """
        Parse a rate such as:

            3/sec
            3/min
            10/hour
            100/day
        """

        try:
            count, period = self.rate.split(
                "/",
                1,
            )
        except ValueError:
            raise ValueError(
                f"Invalid CAPTCHA rate '{self.rate}'. "
                f"Expected format like '3/min'."
            )

        try:
            count = int(count)
        except ValueError:
            raise ValueError(
                f"Invalid request count "
                f"in CAPTCHA rate '{self.rate}'."
            )

        if count <= 0:
            raise ValueError(
                "CAPTCHA rate count must "
                "be greater than zero."
            )

        period = period.strip().lower()

        if period not in self.PERIODS:
            supported = ", ".join(
                self.PERIODS.keys()
            )

            raise ValueError(
                f"Unsupported CAPTCHA period "
                f"'{period}'. "
                f"Supported periods: {supported}"
            )

        return count, self.PERIODS[period]

    def _get_key(self, identifier):
        """
        Build the cache key for this scope
        and identifier.
        """

        return (
            f"{self.RATE_PREFIX}:"
            f"{self.scope}:"
            f"{identifier}"
        )

    def exceeded(self, identifier):
        """
        Increment the request counter and determine
        whether the CAPTCHA threshold has been exceeded.
        """

        key = self._get_key(identifier)

        current = cache.get(key, 0)

        if current >= self.max_requests:
            return True

        try:
            cache.incr(key)

        except ValueError:
            cache.set(
                key,
                1,
                timeout=self.time_range,
            )

        return False

    def reset(self, identifier):
        """
        Reset the rate counter for an identifier.
        """

        key = self._get_key(identifier)

        cache.delete(key)