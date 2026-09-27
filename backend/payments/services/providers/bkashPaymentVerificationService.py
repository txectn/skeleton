import requests

from django.conf import settings
from django.core.cache import cache
from rest_framework.exceptions import ValidationError

from ...models import PaymentAttempt

class BkashPaymentVerificationService:

    TOKEN_CACHE_KEY = "bkash_access_token"
    TOKEN_CACHE_TIMEOUT = 3300

    EXECUTE_PAYMENT_PATH = (
        "/tokenized/checkout/execute"
    )

    PAYMENT_STATUS_PATH = (
        "/tokenized/checkout/payment/status"
    )

    SUCCESS_CALLBACK_STATUS = "success"

    FAILURE_CALLBACK_STATUSES = {
        "failure",
        "cancel",
    }

    COMPLETED_TRANSACTION_STATUS = "Completed"

    @staticmethod
    def _get_url(path):
        return (
            f"{settings.BKASH_BASE_URL}"
            f"{path}"
        )

    # ---------------------------------------------------------
    # Callback Data Validation
    # ---------------------------------------------------------

    @staticmethod
    def validate_data(data):

        if not isinstance(data, dict):
            raise ValidationError(
                {
                    "payment": (
                        "Invalid bKash callback data."
                    )
                }
            )

        payment_id = data.get("paymentID")
        status = data.get("status")

        if not payment_id:
            raise ValidationError(
                {
                    "payment": (
                        "bKash payment ID is required."
                    )
                }
            )

        if not isinstance(payment_id, str):
            raise ValidationError(
                {
                    "payment": (
                        "Invalid bKash payment ID."
                    )
                }
            )

        payment_id = payment_id.strip()

        if not payment_id:
            raise ValidationError(
                {
                    "payment": (
                        "bKash payment ID is required."
                    )
                }
            )

        if not status:
            raise ValidationError(
                {
                    "payment": (
                        "bKash payment status is required."
                    )
                }
            )

        if not isinstance(status, str):
            raise ValidationError(
                {
                    "payment": (
                        "Invalid bKash payment status."
                    )
                }
            )

        status = status.strip().lower()

        allowed_statuses = {
            BkashPaymentVerificationService.SUCCESS_CALLBACK_STATUS,
            *BkashPaymentVerificationService.FAILURE_CALLBACK_STATUSES,
        }

        if status not in allowed_statuses:
            raise ValidationError(
                {
                    "payment": (
                        "Invalid bKash payment status."
                    )
                }
            )

        return {
            "payment_id": payment_id,
            "status": status,
        }

    # ---------------------------------------------------------
    # Identify Provider
    # ---------------------------------------------------------

    @staticmethod
    def can_handle(data):

        if not isinstance(data, dict):
            return False

        return bool(data.get("paymentID"))

    # ---------------------------------------------------------
    # Access Token
    # ---------------------------------------------------------

    @staticmethod
    def get_access_token():

        access_token = cache.get(
            BkashPaymentVerificationService.TOKEN_CACHE_KEY,
        )

        if access_token:
            return access_token

        url = BkashPaymentVerificationService._get_url(
            "/tokenized/checkout/token/grant",
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

        expires_in = result.get(
            "expires_in",
            BkashPaymentVerificationService.TOKEN_CACHE_TIMEOUT,
        )

        try:
            expires_in = int(expires_in)
        except (TypeError, ValueError):
            expires_in = (
                BkashPaymentVerificationService.TOKEN_CACHE_TIMEOUT
            )

        cache_timeout = min(
            expires_in - 60,
            BkashPaymentVerificationService.TOKEN_CACHE_TIMEOUT,
        )

        if cache_timeout <= 0:
            cache_timeout = 60

        cache.set(
            BkashPaymentVerificationService.TOKEN_CACHE_KEY,
            access_token,
            cache_timeout,
        )

        return access_token

    # ---------------------------------------------------------
    # Find Payment Attempt
    # ---------------------------------------------------------

    @staticmethod
    def get_payment_attempt(payment_id):

        try:
            return (
                PaymentAttempt.objects
                .select_related(
                    "payment__order",
                )
                .get(
                    provider="bkash",
                    provider_payment_id=payment_id,
                )
            )
        except PaymentAttempt.DoesNotExist:
            raise ValidationError(
                {
                    "payment": (
                        "bKash payment attempt was not found."
                    )
                }
            )

    # ---------------------------------------------------------
    # Execute Payment
    # ---------------------------------------------------------

    @staticmethod
    def execute_payment(payment_id):

        access_token = (
            BkashPaymentVerificationService
            .get_access_token()
        )

        url = BkashPaymentVerificationService._get_url(
            BkashPaymentVerificationService.EXECUTE_PAYMENT_PATH,
        )

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": access_token,
            "X-APP-Key": settings.BKASH_APP_KEY,
        }

        data = {
            "paymentID": payment_id,
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
                        "Invalid payment verification "
                        "response received from bKash."
                    )
                }
            )

        if not response.ok:
            raise ValidationError(
                {
                    "payment": (
                        "bKash payment execution failed."
                    )
                }
            )

        return result

    # ---------------------------------------------------------
    # Verify
    # ---------------------------------------------------------

    @staticmethod
    def verify(data):

        validated_data = (
            BkashPaymentVerificationService
            .validate_data(data)
        )

        payment_id = validated_data["payment_id"]
        callback_status = validated_data["status"]

        payment_attempt = (
            BkashPaymentVerificationService
            .get_payment_attempt(payment_id)
        )

        # -----------------------------------------------------
        # Already Paid
        # -----------------------------------------------------

        if (
            payment_attempt.payment.status
            == payment_attempt.payment.Status.PAID
        ):
            return {
                "success": True,
                "payment_attempt": payment_attempt,
                "transaction_id": (
                    payment_attempt.transaction_id
                ),
            }

        # -----------------------------------------------------
        # Customer Failed / Cancelled
        # -----------------------------------------------------

        if callback_status in (
            BkashPaymentVerificationService
            .FAILURE_CALLBACK_STATUSES
        ):
            return {
                "success": False,
                "payment_attempt": payment_attempt,
                "transaction_id": None,
            }

        # -----------------------------------------------------
        # Success Callback
        # -----------------------------------------------------

        result = (
            BkashPaymentVerificationService
            .execute_payment(payment_id)
        )

        # -----------------------------------------------------
        # Validate Provider Response
        # -----------------------------------------------------

        response_payment_id = result.get(
            "paymentID"
        )

        if response_payment_id != payment_id:
            raise ValidationError(
                {
                    "payment": (
                        "bKash returned an invalid "
                        "payment ID."
                    )
                }
            )

        status_code = result.get(
            "statusCode"
        )

        if status_code != "0000":
            return {
                "success": False,
                "payment_attempt": payment_attempt,
                "transaction_id": result.get(
                    "trxID"
                ),
            }

        transaction_status = result.get(
            "transactionStatus"
        )

        transaction_id = result.get(
            "trxID"
        )

        if (
            transaction_status
            != BkashPaymentVerificationService
            .COMPLETED_TRANSACTION_STATUS
        ):
            return {
                "success": False,
                "payment_attempt": payment_attempt,
                "transaction_id": transaction_id,
            }

        # -----------------------------------------------------
        # Validate Payment Amount
        # -----------------------------------------------------

        provider_amount = result.get("amount")

        if provider_amount is None:
            raise ValidationError(
                {
                    "payment": (
                        "bKash verification response "
                        "does not contain an amount."
                    )
                }
            )

        if str(provider_amount) != str(
            payment_attempt.payment.order.total
        ):
            raise ValidationError(
                {
                    "payment": (
                        "bKash payment amount does not "
                        "match the order amount."
                    )
                }
            )

        # -----------------------------------------------------
        # Validate Currency
        # -----------------------------------------------------

        provider_currency = result.get(
            "currency"
        )

        if provider_currency != "BDT":
            raise ValidationError(
                {
                    "payment": (
                        "bKash payment currency does "
                        "not match the order currency."
                    )
                }
            )

        # -----------------------------------------------------
        # Successful Verification
        # -----------------------------------------------------

        return {
            "success": True,
            "payment_attempt": payment_attempt,
            "transaction_id": transaction_id,
        }