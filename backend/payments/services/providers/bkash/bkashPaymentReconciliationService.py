import requests

from django.conf import settings
from django.core.cache import cache
from rest_framework.exceptions import ValidationError

class BkashPaymentReconciliationService:
    """Handles bKash payment reconciliation through Query Payment."""

    TOKEN_CACHE_KEY = "bkash_access_token"
    TOKEN_CACHE_TIMEOUT = 3300

    QUERY_PAYMENT_PATH = (
        "/v2/tokenized-checkout/query/payment"
    )

    @staticmethod
    def can_handle(provider):
        return provider == "bkash"

    @staticmethod
    def get_access_token():
        access_token = cache.get(
            BkashPaymentReconciliationService.TOKEN_CACHE_KEY,
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
            BkashPaymentReconciliationService.TOKEN_CACHE_KEY,
            access_token,
            BkashPaymentReconciliationService.TOKEN_CACHE_TIMEOUT,
        )

        return access_token

    @staticmethod
    def reconcile(payment_attempt):
        """
        Query bKash for the current state of a payment.

        This is primarily used when Execute Payment times out
        or when the local payment state is uncertain.
        """

        payment_id = payment_attempt.provider_payment_id

        if not payment_id:
            raise ValidationError(
                {
                    "payment": (
                        "bKash payment ID is missing."
                    )
                }
            )

        access_token = (
            BkashPaymentReconciliationService.get_access_token()
        )

        url = (
            f"{settings.BKASH_BASE_URL}"
            f"{BkashPaymentReconciliationService.QUERY_PAYMENT_PATH}"
        )

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": access_token,
            "X-APP-Key": settings.BKASH_APP_KEY,
        }

        data = {
            "paymentId": payment_id,
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
                        "Unable to connect to bKash "
                        "for payment reconciliation."
                    )
                }
            )

        try:
            result = response.json()
        except ValueError:
            raise ValidationError(
                {
                    "payment": (
                        "Invalid payment query response "
                        "received from bKash."
                    )
                }
            )

        if not response.ok:
            raise ValidationError(
                {
                    "payment": (
                        result.get(
                            "errorMessageEn",
                            "Unable to retrieve "
                            "bKash payment status.",
                        )
                    )
                }
            )

        transaction_status = result.get(
            "transactionStatus",
        )

        transaction_id = result.get(
            "trxId",
        )

        if transaction_status == "Completed":
            return {
                "status": "success",
                "transaction_id": transaction_id,
                "provider_response": result,
            }

        if transaction_status == "Initiated":
            return {
                "status": "pending",
                "transaction_id": transaction_id,
                "provider_response": result,
            }

        return {
            "status": "pending",
            "transaction_id": transaction_id,
            "provider_response": result,
        }