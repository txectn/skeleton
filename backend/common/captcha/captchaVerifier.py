import requests

from django.conf import settings

class CaptchaVerifier:

    VERIFY_URL = (
        "https://www.google.com/recaptcha/api/siteverify"
    )

    TIMEOUT = 5

    def __init__(self, secret_key=None):
        self.secret_key = (
            secret_key
            or settings.RECAPTCHA_SECRET_KEY
        )

    def verify(self, token, ip=None):
        """
        Verify a CAPTCHA token with Google.
        """

        if not token:
            return False

        data = {
            "secret": self.secret_key,
            "response": token,
        }

        if ip:
            data["remoteip"] = ip

        try:
            response = requests.post(
                self.VERIFY_URL,
                data=data,
                timeout=self.TIMEOUT,
            )

            response.raise_for_status()

            result = response.json()

        except (
            requests.RequestException,
            ValueError,
        ):
            return False

        return result.get("success", False)