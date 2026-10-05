import requests

from django.conf import settings
from rest_framework.exceptions import ValidationError

from ....models import PaymentAttempt
from .bkashTokenService import BkashTokenService

class BkashPaymentExecutionService:
    """Handles bKash payment execution and verification."""

    EXECUTE_PAYMENT_PATH = (
        "/v2/tokenized-checkout/payment/execute"
    )

    @staticmethod
    def _get_url(path):
        return (
            f"{settings.BKASH_BASE_URL}"
            f"{path}"
        )

    @classmethod
    def execute_payment(
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

        except:
            raise ValidationError(
                {
                    "message": (
                        "bKash payment attempt was not found."
                    ),
                    "provider_payment_id": payment_id,
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
                    "payment": (
                        "Unable to authenticate with bKash."
                    )
                }
            )

        # ---------------------------------------------------------
        # URL
        # ---------------------------------------------------------

        url = cls._get_url(
            cls.EXECUTE_PAYMENT_PATH
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
        # Execute Payment
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
                    "payment": (
                        "The bKash payment execution timed out. "
                        "Please verify the payment status."
                    ),
                    "payment_id": payment_id,
                    "status": "pending",
                }
            )

        except requests.RequestException:
            raise ValidationError(
                {
                    "payment": (
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
                    "payment": (
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
                "bKash payment execution failed.",
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
                    "payment": error_message,
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
                    "payment": (
                        "The bKash payment ID does not match."
                    )
                }
            )

        # ---------------------------------------------------------
        # Validate Transaction Status
        # ---------------------------------------------------------

        transaction_status = result.get(
            "transactionStatus"
        )

        if transaction_status != "Completed":
            raise ValidationError(
                {
                    "payment": (
                        "bKash did not complete the payment."
                    ),
                    "transaction_status": (
                        transaction_status
                    ),
                }
            )

        # ---------------------------------------------------------
        # Transaction ID
        # ---------------------------------------------------------

        trx_id = result.get(
            "trxId"
        )

        if not trx_id:
            raise ValidationError(
                {
                    "payment": (
                        "bKash did not return a transaction ID."
                    )
                }
            )

        # ---------------------------------------------------------
        # Validate Amount
        # ---------------------------------------------------------

        response_amount = result.get(
            "amount"
        )

        if str(response_amount) != str(order.total):
            raise ValidationError(
                {
                    "payment": (
                        "The bKash payment amount does not "
                        "match the order amount."
                    )
                }
            )

        # ---------------------------------------------------------
        # Validate Currency
        # ---------------------------------------------------------

        currency = result.get(
            "currency"
        )

        if currency != "BDT":
            raise ValidationError(
                {
                    "payment": (
                        "The bKash payment currency does "
                        "not match the expected currency."
                    ),
                    "currency": currency,
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
            "trx_id": trx_id,
            "amount": response_amount,
            "currency": currency,
            "transaction_status": transaction_status,
        }