import requests

from django.conf import settings
from django.core.cache import cache
from rest_framework.exceptions import ValidationError

class BkashPaymentService:

    TOKEN_CACHE_KEY = "bkash_access_token"
    TOKEN_CACHE_TIMEOUT = 3300

    @staticmethod
    def get_access_token():

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

        response = requests.post(
            url,
            headers=headers,
            json=data,
            timeout=30,
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

        result = response.json()

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
            BkashPaymentService.TOKEN_CACHE_KEY,
            access_token,
            BkashPaymentService.TOKEN_CACHE_TIMEOUT,
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

        url = (
            f"{settings.BKASH_BASE_URL}"
            "/tokenized/checkout/create"
        )

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": access_token,
            "X-APP-Key": settings.BKASH_APP_KEY,
        }

        data = {
            "amount": str(order.total),
            "currency": "BDT",
            "intent": "sale",
            "merchantInvoiceNumber": f"ORDER-{order.id}",
            "callbackURL": settings.BKASH_CALLBACK_URL,
        }

        try:
            response = requests.post(
                url,
                headers=headers,
                json=data,
                timeout=30,
            )
        except requests.RequestException:
            payment_attempt.status = (
                payment_attempt.Status.FAILED
            )
            payment_attempt.save(
                update_fields=[
                    "status",
                    "updated_at",
                ]
            )

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
            payment_attempt.status = (
                payment_attempt.Status.FAILED
            )
            payment_attempt.save(
                update_fields=[
                    "status",
                    "updated_at",
                ]
            )

            raise ValidationError(
                {
                    "payment": (
                        "Invalid response received "
                        "from bKash."
                    )
                }
            )

        if not response.ok:
            payment_attempt.status = (
                payment_attempt.Status.FAILED
            )
            payment_attempt.save(
                update_fields=[
                    "status",
                    "updated_at",
                ]
            )

            raise ValidationError(
                {
                    "payment": (
                        result.get(
                            "statusMessage",
                            "bKash payment creation failed.",
                        )
                    )
                }
            )

        provider_payment_id = result.get("paymentID")
        payment_url = result.get("bkashURL")

        if not provider_payment_id or not payment_url:
            payment_attempt.status = (
                payment_attempt.Status.FAILED
            )
            payment_attempt.save(
                update_fields=[
                    "status",
                    "updated_at",
                ]
            )

            raise ValidationError(
                {
                    "payment": (
                        "Invalid payment response "
                        "received from bKash."
                    )
                }
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