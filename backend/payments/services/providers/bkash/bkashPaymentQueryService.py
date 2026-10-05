import requests

from django.conf import settings
from rest_framework.exceptions import ValidationError

from ....models import PaymentAttempt
from .bkashTokenService import BkashTokenService

class BkashPaymentQueryService:
    """Handles bKash payment status queries."""

    QUERY_PAYMENT_PATH = (
        "/v2/tokenized-checkout/payment/status"
    )

    @staticmethod
    def _get_url(path):
        return (
            f"{settings.BKASH_BASE_URL}"
            f"{path}"
        )

    @classmethod
    def query_payment(
        cls,
        payment_id,
    ):
        # ---------------------------------------------------------
        # Find Payment Attempt
        # ---------------------------------------------------------

        try:
            payment_attempt = (
                PaymentAttempt.objects
                .select_related(
                    "payment",
                    "payment__order",
                )
                .get(
                    provider_payment_id=payment_id,
                    provider="bkash",
                )
            )

        except PaymentAttempt.DoesNotExist:
            raise ValidationError(
                {
                    "message": (
                        "The bKash payment could not be found."
                    )
                }
            )

        payment = payment_attempt.payment
        order = payment.order

        # ---------------------------------------------------------
        # Get bKash ID Token
        # ---------------------------------------------------------

        try:
            id_token = (
                BkashTokenService.get_id_token()
            )

        except Exception:
            raise ValidationError(
                {
                    "message": (
                        "Unable to authenticate with bKash."
                    )
                }
            )

        # ---------------------------------------------------------
        # URL
        # ---------------------------------------------------------

        url = cls._get_url(
            cls.QUERY_PAYMENT_PATH
        )

        # ---------------------------------------------------------
        # Headers
        # ---------------------------------------------------------

        headers = {
            "Authorization": id_token,
            "X-App-Key": settings.BKASH_APP_KEY,
            "Content-Type": "application/json",
        }

        # ---------------------------------------------------------
        # Request Data
        # ---------------------------------------------------------

        payload = {
            "paymentId": payment_id,
        }

        # ---------------------------------------------------------
        # Query Payment
        # ---------------------------------------------------------

        try:
            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=30,
            )

        except requests.Timeout:
            raise ValidationError(
                {
                    "message": (
                        "The bKash payment query timed out."
                    ),
                    "payment_id": payment_id,
                    "status": "pending",
                }
            )

        except requests.RequestException:
            raise ValidationError(
                {
                    "message": (
                        "Unable to connect to bKash."
                    )
                }
            )

        # ---------------------------------------------------------
        # Parse Response
        # ---------------------------------------------------------

        try:
            result = response.json()

        except ValueError:
            raise ValidationError(
                {
                    "message": (
                        "Invalid response received from bKash."
                    )
                }
            )

        # ---------------------------------------------------------
        # bKash API Error
        # ---------------------------------------------------------

        if not response.ok:
            error_message = result.get(
                "errorMessageEn",
                "bKash payment query failed.",
            )

            external_code = result.get(
                "externalCode"
            )

            if external_code:
                error_message = (
                    f"bKash Error ({external_code}): "
                    f"{error_message}"
                )

            raise ValidationError(
                {
                    "message": error_message,
                    "payment_id": payment_id,
                    "external_code": external_code,
                }
            )

        # ---------------------------------------------------------
        # Validate Payment ID
        # ---------------------------------------------------------

        response_payment_id = result.get(
            "paymentId"
        )

        if response_payment_id != payment_id:
            raise ValidationError(
                {
                    "message": (
                        "The bKash payment ID does not match."
                    ),
                    "payment_id": payment_id,
                    "response_payment_id": (
                        response_payment_id
                    ),
                }
            )

        # ---------------------------------------------------------
        # Transaction Status
        # ---------------------------------------------------------

        transaction_status = result.get(
            "transactionStatus"
        )

        if not transaction_status:
            raise ValidationError(
                {
                    "message": (
                        "bKash did not return a "
                        "transaction status."
                    ),
                    "payment_id": payment_id,
                }
            )

        # ---------------------------------------------------------
        # Return Result
        # ---------------------------------------------------------

        return {
            "payment_attempt": payment_attempt,
            "payment": payment,
            "order": order,
            "payment_id": response_payment_id,
            "trx_id": result.get(
                "trxId"
            ),
            "amount": result.get(
                "amount"
            ),
            "currency": result.get(
                "currency"
            ),
            "transaction_status": transaction_status,
            "verification_status": result.get(
                "verificationStatus"
            ),
            "payment_create_time": result.get(
                "paymentCreateTime"
            ),
            "payment_execute_time": result.get(
                "paymentExecuteTime"
            ),
            "payment_update_time": result.get(
                "paymentUpdateTime"
            ),
        }