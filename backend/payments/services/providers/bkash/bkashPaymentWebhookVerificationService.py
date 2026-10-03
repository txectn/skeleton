import json

import requests

from django.conf import settings
from django.core.cache import cache
from rest_framework.exceptions import ValidationError

from ....models import PaymentAttempt

class BkashPaymentWebhookVerificationService:

    TOKEN_CACHE_KEY = "bkash_access_token"
    TOKEN_CACHE_TIMEOUT = 3300

    SEARCH_TRANSACTION_PATH = (
        "/tokenized/checkout/general/searchTransaction"
    )

    COMPLETED_TRANSACTION_STATUS = "Completed"

    # ---------------------------------------------------------
    # URL
    # ---------------------------------------------------------

    @staticmethod
    def _get_url(path):

        return (
            f"{settings.BKASH_BASE_URL}"
            f"{path}"
        )

    # ---------------------------------------------------------
    # Identify Provider
    # ---------------------------------------------------------

    @staticmethod
    def can_handle(data):

        if not isinstance(data, dict):
            return False

        return (
            data.get("Type") == "Notification"
            and bool(data.get("Message"))
        )

    # ---------------------------------------------------------
    # Webhook Data Validation
    # ---------------------------------------------------------

    @staticmethod
    def validate_webhook_data(data):

        if not isinstance(data, dict):

            raise ValidationError(
                {
                    "payment": (
                        "Invalid bKash webhook data."
                    )
                }
            )

        notification_type = data.get("Type")

        if notification_type != "Notification":

            raise ValidationError(
                {
                    "payment": (
                        "Invalid bKash notification type."
                    )
                }
            )

        message = data.get("Message")

        if not message:

            raise ValidationError(
                {
                    "payment": (
                        "bKash webhook message is required."
                    )
                }
            )

        if not isinstance(message, str):

            raise ValidationError(
                {
                    "payment": (
                        "Invalid bKash webhook message."
                    )
                }
            )

        try:

            transaction_data = json.loads(message)

        except (TypeError, ValueError):

            raise ValidationError(
                {
                    "payment": (
                        "Invalid bKash webhook message format."
                    )
                }
            )

        if not isinstance(transaction_data, dict):

            raise ValidationError(
                {
                    "payment": (
                        "Invalid bKash transaction data."
                    )
                }
            )

        return transaction_data

    # ---------------------------------------------------------
    # Access Token
    # ---------------------------------------------------------

    @staticmethod
    def get_access_token():

        access_token = cache.get(
            BkashPaymentWebhookVerificationService.TOKEN_CACHE_KEY,
        )

        if access_token:

            return access_token

        url = BkashPaymentWebhookVerificationService._get_url(
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
            BkashPaymentWebhookVerificationService.TOKEN_CACHE_TIMEOUT,
        )

        try:

            expires_in = int(expires_in)

        except (TypeError, ValueError):

            expires_in = (
                BkashPaymentWebhookVerificationService
                .TOKEN_CACHE_TIMEOUT
            )

        cache_timeout = min(
            expires_in - 60,
            BkashPaymentWebhookVerificationService
            .TOKEN_CACHE_TIMEOUT,
        )

        if cache_timeout <= 0:

            cache_timeout = 60

        cache.set(
            BkashPaymentWebhookVerificationService.TOKEN_CACHE_KEY,
            access_token,
            cache_timeout,
        )

        return access_token

    # ---------------------------------------------------------
    # Find Payment Attempt
    # ---------------------------------------------------------

    @staticmethod
    def get_payment_attempt(
        merchant_invoice_number,
    ):

        try:

            return (
                PaymentAttempt.objects
                .select_related(
                    "payment__order",
                )
                .get(
                    provider="bkash",
                    payment__order__id=merchant_invoice_number,
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
    # Search Transaction
    # ---------------------------------------------------------

    @staticmethod
    def search_transaction(transaction_id):

        access_token = (
            BkashPaymentWebhookVerificationService
            .get_access_token()
        )

        url = BkashPaymentWebhookVerificationService._get_url(
            BkashPaymentWebhookVerificationService
            .SEARCH_TRANSACTION_PATH,
        )

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": access_token,
            "X-APP-Key": settings.BKASH_APP_KEY,
        }

        data = {
            "trxID": transaction_id,
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
                        "for transaction verification."
                    )
                }
            )

        try:

            result = response.json()

        except ValueError:

            raise ValidationError(
                {
                    "payment": (
                        "Invalid transaction verification "
                        "response received from bKash."
                    )
                }
            )

        if not response.ok:

            raise ValidationError(
                {
                    "payment": (
                        "Unable to verify the bKash transaction."
                    )
                }
            )

        return result

    # ---------------------------------------------------------
    # Verify Webhook
    # ---------------------------------------------------------

    @staticmethod
    def verify_webhook(data):

        transaction_data = (
            BkashPaymentWebhookVerificationService
            .validate_webhook_data(data)
        )

        transaction_status = transaction_data.get(
            "transactionStatus"
        )

        transaction_id = transaction_data.get(
            "trxID"
        )

        merchant_invoice_number = transaction_data.get(
            "merchantInvoiceNumber"
        )

        amount = transaction_data.get(
            "amount"
        )

        currency = transaction_data.get(
            "currency"
        )

        # -----------------------------------------------------
        # Required Fields
        # -----------------------------------------------------

        if not transaction_id:

            raise ValidationError(
                {
                    "payment": (
                        "bKash transaction ID is required."
                    )
                }
            )

        if not merchant_invoice_number:

            raise ValidationError(
                {
                    "payment": (
                        "bKash merchant invoice number "
                        "is required."
                    )
                }
            )

        if amount is None:

            raise ValidationError(
                {
                    "payment": (
                        "bKash transaction amount is required."
                    )
                }
            )

        if not currency:

            raise ValidationError(
                {
                    "payment": (
                        "bKash transaction currency is required."
                    )
                }
            )

        # -----------------------------------------------------
        # Find Local Payment Attempt
        # -----------------------------------------------------

        payment_attempt = (
            BkashPaymentWebhookVerificationService
            .get_payment_attempt(
                merchant_invoice_number,
            )
        )

        payment = payment_attempt.payment
        order = payment.order

        # -----------------------------------------------------
        # Already Paid
        # -----------------------------------------------------

        if payment.status == payment.Status.PAID:

            return {
                "success": True,
                "payment_attempt": payment_attempt,
                "transaction_id": (
                    payment_attempt.transaction_id
                    or transaction_id
                ),
            }

        # -----------------------------------------------------
        # Verify Transaction With bKash
        # -----------------------------------------------------

        verified_transaction = (
            BkashPaymentWebhookVerificationService
            .search_transaction(
                transaction_id,
            )
        )

        verified_transaction_id = (
            verified_transaction.get("trxID")
        )

        verified_status = (
            verified_transaction.get("transactionStatus")
        )

        verified_amount = (
            verified_transaction.get("amount")
        )

        verified_currency = (
            verified_transaction.get("currency")
        )

        verified_invoice = (
            verified_transaction.get(
                "merchantInvoiceNumber"
            )
        )

        # -----------------------------------------------------
        # Verify Transaction ID
        # -----------------------------------------------------

        if verified_transaction_id != transaction_id:

            raise ValidationError(
                {
                    "payment": (
                        "bKash transaction ID does not "
                        "match the verified transaction."
                    )
                }
            )

        # -----------------------------------------------------
        # Verify Merchant Invoice
        # -----------------------------------------------------

        if verified_invoice != merchant_invoice_number:

            raise ValidationError(
                {
                    "payment": (
                        "bKash merchant invoice number does "
                        "not match the verified transaction."
                    )
                }
            )

        # -----------------------------------------------------
        # Verify Transaction Status
        # -----------------------------------------------------

        if (
            verified_status
            != BkashPaymentWebhookVerificationService
            .COMPLETED_TRANSACTION_STATUS
        ):

            return {
                "success": False,
                "payment_attempt": payment_attempt,
                "transaction_id": transaction_id,
            }

        # -----------------------------------------------------
        # Verify Amount
        # -----------------------------------------------------

        if str(verified_amount) != str(order.total):

            raise ValidationError(
                {
                    "payment": (
                        "bKash payment amount does not "
                        "match the order amount."
                    )
                }
            )

        # -----------------------------------------------------
        # Verify Currency
        # -----------------------------------------------------

        if verified_currency != "BDT":

            raise ValidationError(
                {
                    "payment": (
                        "bKash payment currency does "
                        "not match the order currency."
                    )
                }
            )

        # -----------------------------------------------------
        # Verify Webhook Against bKash Response
        # -----------------------------------------------------

        if str(amount) != str(verified_amount):

            raise ValidationError(
                {
                    "payment": (
                        "bKash webhook amount does not "
                        "match the verified transaction."
                    )
                }
            )

        if currency != verified_currency:

            raise ValidationError(
                {
                    "payment": (
                        "bKash webhook currency does not "
                        "match the verified transaction."
                    )
                }
            )

        if transaction_status != verified_status:

            raise ValidationError(
                {
                    "payment": (
                        "bKash webhook transaction status "
                        "does not match the verified "
                        "transaction."
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