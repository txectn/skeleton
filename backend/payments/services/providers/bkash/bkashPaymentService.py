import requests

from django.conf import settings
from rest_framework.exceptions import ValidationError

from .bkashTokenService import BkashTokenService

class BkashPaymentService:
    """Handles bKash payment creation."""

    CREATE_PAYMENT_PATH = "/tokenized/checkout/create"

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

    @classmethod
    def _raise_payment_error(
        cls,
        payment_attempt,
        message,
    ):
        cls._mark_attempt_failed(
            payment_attempt,
        )

        raise ValidationError(
            {
                "payment": message,
            }
        )

    @classmethod
    def create_payment(
        cls,
        order,
        payment,
        payment_attempt,
    ):
        """
        Create a bKash payment for the given order.

        The token lifecycle is handled entirely by
        BkashTokenService.
        """

        try:
            id_token = (
                BkashTokenService.get_id_token()
            )

        except Exception:
            cls._raise_payment_error(
                payment_attempt,
                "Unable to authenticate with bKash.",
            )

        url = cls._get_url(
            cls.CREATE_PAYMENT_PATH,
        )

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": id_token,
            "X-APP-Key": settings.BKASH_APP_KEY,
        }

        data = {
            "mode": "0011",
            "payerReference": (
                f"PAYMENT-{payment_attempt.id}"
            ),
            "callbackURL": (
                settings.BKASH_CALLBACK_URL
            ),
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
            cls._raise_payment_error(
                payment_attempt,
                "Unable to connect to bKash.",
            )

        try:
            result = response.json()

        except ValueError:
            cls._raise_payment_error(
                payment_attempt,
                "Invalid response received from bKash.",
            )

        if not response.ok:
            cls._raise_payment_error(
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
            cls._raise_payment_error(
                payment_attempt,
                "bKash did not return a payment ID.",
            )

        if not payment_url:
            cls._raise_payment_error(
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
            "provider_payment_id": provider_payment_id,
        }