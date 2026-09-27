import requests

from django.conf import settings
from django.core.cache import cache
from rest_framework.exceptions import ValidationError

class BkashPaymentService:

    TOKEN_CACHE_KEY = "bkash_access_token"
    TOKEN_CACHE_TIMEOUT = 3300

    CREATE_PAYMENT_PATH = "/tokenized/checkout/create"
    TOKEN_GRANT_PATH = "/tokenized/checkout/token/grant"

    @staticmethod
    def _get_url(path):

        return (
            f"{settings.BKASH_BASE_URL}"
            f"{path}"
        )

    @staticmethod
    def _mark_attempt_failed(payment_attempt):

        if payment_attempt.status != (
            payment_attempt.Status.FAILED
        ):
            payment_attempt.status = (
                payment_attempt.Status.FAILED
            )

            payment_attempt.save(
                update_fields=[
                    "status",
                    "updated_at",
                ]
            )

    @staticmethod
    def _raise_payment_error(
        payment_attempt,
        message,
    ):

        BkashPaymentService._mark_attempt_failed(
            payment_attempt,
        )

        raise ValidationError(
            {
                "payment": message,
            }
        )

    @staticmethod
    def get_access_token():

        url = BkashPaymentService._get_url(
            BkashPaymentService.TOKEN_GRANT_PATH,
        )

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "username": settings.BKASH_USERNAME,
            "password": settings.BKASH_PASSWORD,
        }

        data = {
            "app_key": settings.BKASH_APP_KEY,
            "app_secret": settings.BKASH_APP_SECRET,
        }

        try:
            response = requests.post(
                url,
                headers=headers,
                json=data,
                timeout=30,
            )

        except requests.RequestException:
            raise ValidationError(
                {
                    "payment": (
                        "Unable to connect to bKash."
                    )
                }
            )

        try:
            result = response.json()

        except ValueError:
            raise ValidationError(
                {
                    "payment": (
                        "Invalid authentication response "
                        "received from bKash."
                    )
                }
            )

        if not response.ok:
            raise ValidationError(
                {
                    "payment": (
                        "Unable to authenticate with "
                        "bKash."
                    )
                }
            )

        access_token = result.get("id_token")

        if not access_token:
            raise ValidationError(
                {
                    "payment": (
                        "bKash authentication failed."
                    )
                }
            )

        expires_in = result.get(
            "expires_in",
            BkashPaymentService.TOKEN_CACHE_TIMEOUT,
        )

        try:
            expires_in = int(expires_in)

        except (TypeError, ValueError):
            expires_in = (
                BkashPaymentService.TOKEN_CACHE_TIMEOUT
            )

        cache_timeout = min(
            expires_in - 60,
            BkashPaymentService.TOKEN_CACHE_TIMEOUT,
        )

        if cache_timeout <= 0:
            cache_timeout = 60

        cache.set(
            BkashPaymentService.TOKEN_CACHE_KEY,
            access_token,
            cache_timeout,
        )

        return access_token

    @staticmethod
    def create_payment(
        order,
        payment,
        payment_attempt,
    ):

        access_token = cache.get(
            BkashPaymentService.TOKEN_CACHE_KEY,
        )

        if not access_token:
            access_token = (
                BkashPaymentService.get_access_token()
            )

        url = BkashPaymentService._get_url(
            BkashPaymentService.CREATE_PAYMENT_PATH,
        )

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": access_token,
            "X-APP-Key": settings.BKASH_APP_KEY,
        }

        data = {
            "mode": "0011",
            "payerReference": (
                f"PAYMENT-{payment_attempt.id}"
            ),
            "callbackURL": settings.BKASH_CALLBACK_URL,
            "amount": str(order.total),
            "currency": "BDT",
            "intent": "sale",
            "merchantInvoiceNumber": (
                f"ORDER-{order.id}"
            ),
        }

        try:
            response = requests.post(
                url,
                headers=headers,
                json=data,
                timeout=30,
            )

        except requests.RequestException:
            BkashPaymentService._raise_payment_error(
                payment_attempt,
                "Unable to connect to bKash.",
            )

        try:
            result = response.json()

        except ValueError:
            BkashPaymentService._raise_payment_error(
                payment_attempt,
                "Invalid response received from bKash.",
            )

        if not response.ok:
            BkashPaymentService._raise_payment_error(
                payment_attempt,
                "bKash payment creation failed.",
            )

        provider_payment_id = result.get(
            "paymentID"
        )

        payment_url = result.get(
            "bkashURL"
        )

        if not provider_payment_id:
            BkashPaymentService._raise_payment_error(
                payment_attempt,
                "bKash did not return a payment ID.",
            )

        if not payment_url:
            BkashPaymentService._raise_payment_error(
                payment_attempt,
                "bKash did not return a payment URL.",
            )

        payment_attempt.provider_payment_id = (
            provider_payment_id
        )

        payment_attempt.save(
            update_fields=[
                "provider_payment_id",
                "updated_at",
            ]
        )

        return {
            "payment_url": payment_url,
        }
