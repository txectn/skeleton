import logging

import requests
from django.conf import settings

from .bkashTokenService import BkashTokenService

logger = logging.getLogger(__name__)

class BkashRefundService:
    """Handles bKash refund operations."""

    PROVIDER = "bkash"

    REFUND_URL = (
        "https://tokenized.sandbox.bka.sh/"
        "v2/tokenized-checkout/refund/payment/transaction"
    )

    TIMEOUT = 30

    @classmethod
    def select_service(cls, provider):
        return provider == cls.PROVIDER

    @classmethod
    def refund(cls, *, payment_attempt):
        """
        Execute a full bKash refund for a payment attempt.

        This service only communicates with bKash.
        It does not modify Payment, PaymentAttempt, or Order.
        """

        payment = payment_attempt.payment
        order = payment.order

        payment_id = payment_attempt.provider_payment_id
        trx_id = payment_attempt.transaction_id
        refund_amount = order.total

        if not payment_id:
            return {
                "success": False,
                "pending": False,
                "message": "bKash payment ID is missing.",
            }

        if not trx_id:
            return {
                "success": False,
                "pending": False,
                "message": "bKash transaction ID is missing.",
            }

        token = BkashTokenService.get_token()

        headers = {
            "Authorization": token,
            "X-APP-Key": settings.BKASH_APP_KEY,
            "Content-Type": "application/json",
        }

        payload = {
            "paymentId": payment_id,
            "refundAmount": str(refund_amount),
            "trxId": trx_id,
            "sku": str(order.id),
            "reason": "Order cancelled",
        }

        try:
            response = requests.post(
                cls.REFUND_URL,
                headers=headers,
                json=payload,
                timeout=cls.TIMEOUT,
            )

        except requests.Timeout:
            logger.warning(
                "bKash refund request timed out for payment attempt %s.",
                payment_attempt.id,
            )

            return {
                "success": False,
                "pending": True,
                "message": "bKash refund request timed out.",
            }

        except requests.RequestException:
            logger.exception(
                "bKash refund request failed for payment attempt %s.",
                payment_attempt.id,
            )

            return {
                "success": False,
                "pending": False,
                "message": "Unable to connect to bKash refund API.",
            }

        try:
            data = response.json()

        except ValueError:
            logger.error(
                "Invalid response received from bKash refund API "
                "for payment attempt %s.",
                payment_attempt.id,
            )

            return {
                "success": False,
                "pending": False,
                "message": "Invalid response from bKash.",
            }

        if (
            response.ok
            and data.get("refundTransactionStatus") == "Completed"
        ):
            return {
                "success": True,
                "pending": False,
                "refund_trx_id": data.get("refundTrxId"),
                "refund_amount": data.get("refundAmount"),
                "original_trx_id": data.get("originalTrxId"),
                "original_trx_amount": data.get("originalTrxAmount"),
                "currency": data.get("currency"),
                "completed_time": data.get("completedTime"),
                "sku": data.get("sku"),
                "reason": data.get("reason"),
                "data": data,
            }

        return {
            "success": False,
            "pending": False,
            "message": data.get(
                "errorMessageEn",
                "bKash refund failed.",
            ),
            "external_code": data.get("externalCode"),
            "data": data,
        }