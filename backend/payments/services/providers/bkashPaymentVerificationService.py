import requests

from django.conf import settings
from django.core.cache import cache
from rest_framework.exceptions import ValidationError

from ...models import PaymentAttempt

class BkashPaymentVerificationService:

    TOKEN_CACHE_KEY = "bkash_access_token"
    TOKEN_CACHE_TIMEOUT = 3300

    @staticmethod
    def can_handle(data):

        payment_id = data.get("paymentID")

        return bool(payment_id)

    @staticmethod
    def get_access_token():

        access_token = cache.get(
            BkashPaymentVerificationService.TOKEN_CACHE_KEY,
        )

        if access_token:
            return access_token

        url = (
            f"{settings.BKASH_BASE_URL}"
            "/tokenized/checkout/token/grant"
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
                        "Unable to authenticate with bKash."
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

        cache.set(
            BkashPaymentVerificationService.TOKEN_CACHE_KEY,
            access_token,
            BkashPaymentVerificationService.TOKEN_CACHE_TIMEOUT,
        )

        return access_token

    @staticmethod
    def verify(data):

        payment_id = data.get("paymentID")

        if not payment_id:
            raise ValidationError(
                {
                    "payment": (
                        "bKash payment ID is required."
                    )
                }
            )

        try:
            payment_attempt = PaymentAttempt.objects.select_related(
                "payment__order",
            ).get(
                provider="bkash",
                provider_payment_id=payment_id,
            )
        except PaymentAttempt.DoesNotExist:
            raise ValidationError(
                {
                    "payment": (
                        "bKash payment attempt was not found."
                    )
                }
            )

        access_token = (
            BkashPaymentVerificationService.get_access_token()
        )

        url = (
            f"{settings.BKASH_BASE_URL}"
            "/tokenized/checkout/execute"
        )

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": access_token,
            "X-APP-Key": settings.BKASH_APP_KEY,
        }

        request_data = {
            "paymentID": payment_id,
        }

        try:
            response = requests.post(
                url,
                headers=headers,
                json=request_data,
                timeout=30,
            )
        except requests.RequestException:
            raise ValidationError(
                {
                    "payment": (
                        "Unable to connect to bKash "
                        "for payment verification."
                    )
                }
            )

        try:
            result = response.json()
        except ValueError:
            raise ValidationError(
                {
                    "payment": (
                        "Invalid payment verification response "
                        "received from bKash."
                    )
                }
            )

        if not response.ok:
            raise ValidationError(
                {
                    "payment": (
                        result.get(
                            "statusMessage",
                            "bKash payment verification failed.",
                        )
                    )
                }
            )

        transaction_status = result.get(
            "transactionStatus",
        )

        transaction_id = result.get(
            "trxID",
        )

        if transaction_status != "Completed":

            return {
                "success": False,
                "payment_attempt": payment_attempt,
                "transaction_id": transaction_id,
            }

        return {
            "success": True,
            "payment_attempt": payment_attempt,
            "transaction_id": transaction_id,
        }