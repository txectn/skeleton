from ipware import get_client_ip
from django.conf import settings
from rest_framework.exceptions import PermissionDenied

from .captchaLock import CaptchaLock
from .captchaRate import CaptchaRate
from .captchaVerifier import CaptchaVerifier

class CaptchaRunner:

    TOKEN_FIELD = "captcha_token"

    DEFAULT_LOCK_TTL = 30
    DEFAULT_BYPASS_TTL = 90

    def __init__(self, request, scope):
        self.request = request
        self.scope = scope

        self.ip = self._get_ip()

        self.lock_ttl = getattr(
            settings,
            "CAPTCHA_LOCK_TTL",
            self.DEFAULT_LOCK_TTL,
        )

        self.bypass_ttl = getattr(
            settings,
            "CAPTCHA_BYPASS_TTL",
            self.DEFAULT_BYPASS_TTL,
        )

        self.rate = CaptchaRate(
            scope=self.scope,
        )

        self.lock = CaptchaLock(
            identifier=self.ip,
            scope=self.scope,
        )

        self.verifier = CaptchaVerifier()

    def run(self):
        """
        Run the CAPTCHA protection flow.

        The request is allowed when:
        - CAPTCHA bypass is active.
        - CAPTCHA is not required.
        - CAPTCHA is successfully verified.

        PermissionDenied is raised when
        CAPTCHA is required or invalid.
        """

        # 1. CAPTCHA was solved recently.
        if self.lock.is_bypassed():
            return

        # 2. CAPTCHA lock already exists.
        if self.lock.is_locked():
            self._verify_captcha()
            return

        # 3. Check the configured CAPTCHA rate.
        if self.rate.exceeded(self.ip):
            self.lock.lock(self.lock_ttl)

        # The request that creates the lock
        # is still allowed.
        return

    def _verify_captcha(self):
        """
        Verify the CAPTCHA token while the IP
        is in CAPTCHA lock mode.
        """

        token = self._get_token()

        if not token:
            self._reject()

        if not self.verifier.verify(
            token=token,
            ip=self.ip,
        ):
            self._reject()

        # CAPTCHA successfully verified.

        # Remove the current CAPTCHA lock.
        self.lock.clear()

        # Reset the CAPTCHA rate counter.
        self.rate.reset(self.ip)

        # Temporarily bypass CAPTCHA.
        self.lock.bypass(self.bypass_ttl)

    def _get_token(self):
        """
        Get the CAPTCHA token from the request body
        or query parameters.
        """

        token = None

        if hasattr(self.request, "data"):
            token = self.request.data.get(
                self.TOKEN_FIELD
            )

        if not token and hasattr(
            self.request,
            "query_params",
        ):
            token = self.request.query_params.get(
                self.TOKEN_FIELD
            )

        return token

    def _get_ip(self):
        """
        Get the client's IP address.
        """

        ip, _ = get_client_ip(self.request)

        if not ip:
            return "unknown"

        return ip

    def _reject(self):
        """
        Reject the request because CAPTCHA
        verification is required or failed.
        """

        raise PermissionDenied(
            detail={
                "success": False,
                "captcha_required": True,
                "message": (
                    "CAPTCHA verification required."
                ),
            }
        )
    

'''
Usage:

1. Configure CAPTCHA rates in settings.py:

    CAPTCHA_RATES = {
        "auth_captcha": "3/min",
        "product_captcha": "10/min",
        "oauth_captcha": "5/hour",
    }

    # Optional: defaults are 30s and 90s
    CAPTCHA_LOCK_TTL = 30
    CAPTCHA_BYPASS_TTL = 90


2. Use in any DRF view (GET, POST, PUT, PATCH, DELETE):

    CaptchaRunner(
        request=request,
        scope="product_captcha",
    ).run()


3. The scope selects the rate from CAPTCHA_RATES.

   Example:
       "product_captcha" → "10/min"

   Different views/actions can use different scopes.


    # In get view.
    def initial(self, request, *args, **kwargs):
        CaptchaRunner(
            request=request,
            scope="product_captcha",
        ).run()

        super().initial(
            request,
            *args,
            **kwargs,
        ) 

    
'''