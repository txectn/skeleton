from django.core.cache import cache

class CaptchaLock:

    LOCK_PREFIX = "captcha_lock"
    BYPASS_PREFIX = "captcha_bypass"

    def __init__(self, identifier, scope):
        self.identifier = identifier
        self.scope = scope

    @property
    def lock_key(self):
        return (
            f"{self.LOCK_PREFIX}:"
            f"{self.scope}:"
            f"{self.identifier}"
        )

    @property
    def bypass_key(self):
        return (
            f"{self.BYPASS_PREFIX}:"
            f"{self.scope}:"
            f"{self.identifier}"
        )

    def is_locked(self):
        """
        Check whether CAPTCHA is currently required.
        """

        return cache.get(
            self.lock_key,
            False,
        )

    def lock(self, ttl):
        """
        Put the identifier into CAPTCHA lock mode.
        """

        cache.set(
            self.lock_key,
            True,
            timeout=ttl,
        )

    def clear(self):
        """
        Remove the current CAPTCHA lock.
        """

        cache.delete(self.lock_key)

    def is_bypassed(self):
        """
        Check whether the identifier has recently
        passed CAPTCHA.
        """

        return cache.get(
            self.bypass_key,
            False,
        )

    def bypass(self, ttl):
        """
        Temporarily bypass CAPTCHA after
        successful verification.
        """

        cache.set(
            self.bypass_key,
            True,
            timeout=ttl,
        )

    def clear_bypass(self):
        """
        Remove the temporary CAPTCHA bypass.
        """

        cache.delete(self.bypass_key)