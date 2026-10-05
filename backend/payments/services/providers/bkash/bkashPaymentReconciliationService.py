import logging

from rest_framework.exceptions import ValidationError

from .bkashPaymentExecutionService import (
    BkashPaymentExecutionService,
)
from .bkashPaymentQueryService import (
    BkashPaymentQueryService,
)

logger = logging.getLogger(__name__)

class BkashPaymentReconciliationService:
    """
    Handles recovery of unresolved bKash payments.

    Flow:

        1. Try Execute Payment.
        2. If Execute succeeds:
               return success.
        3. If Execute is inconclusive:
               Query Payment.
        4. If Query says Completed:
               return success.
        5. If Query says Initiated:
               return pending.
        6. If Query says a terminal failure status:
               return failed.

    This service does NOT update PaymentAttempt, Payment,
    or Order. Database state changes are handled by
    PaymentReconciliationService.
    """

    PROVIDER = "bkash"

    COMPLETED_STATUS = "Completed"
    INITIATED_STATUS = "Initiated"

    # Add confirmed bKash terminal failure statuses here.
    FAILED_STATUSES = (
        # "Failed",
        # "Cancelled",
    )

    @classmethod
    def can_handle(cls, provider):
        return provider == cls.PROVIDER

    @classmethod
    def reconcile(cls, payment_attempt):

        # ---------------------------------------------------------
        # Validate Payment Attempt
        # ---------------------------------------------------------

        cls._validate_payment_attempt(
            payment_attempt
        )

        payment_id = (
            payment_attempt.provider_payment_id
        )

        # ---------------------------------------------------------
        # Execute Payment First
        # ---------------------------------------------------------

        try:
            execution_result = (
                BkashPaymentExecutionService.execute_payment(
                    payment_id=payment_id,
                )
            )

        except ValidationError as exc:

            logger.warning(
                "bKash payment execution was not conclusive. "
                "payment_id=%s error=%s",
                payment_id,
                exc.detail,
            )

            execution_result = None

        # ---------------------------------------------------------
        # Execute Successful
        # ---------------------------------------------------------

        if execution_result is not None:

            return cls._build_success_result(
                execution_result
            )

        # ---------------------------------------------------------
        # Execute Was Not Conclusive
        # ---------------------------------------------------------
        #
        # We cannot assume the payment failed.
        #
        # Execute may have reached bKash even if our application
        # received a timeout or an error response.
        #
        # Therefore query the provider for the actual state.
        # ---------------------------------------------------------

        return cls._query_payment(
            payment_id=payment_id,
        )

    # =============================================================
    # Validation
    # =============================================================

    @classmethod
    def _validate_payment_attempt(
        cls,
        payment_attempt,
    ):
        if payment_attempt is None:
            raise ValidationError(
                {
                    "payment": (
                        "Payment attempt is required."
                    )
                }
            )

        if payment_attempt.provider != cls.PROVIDER:
            raise ValidationError(
                {
                    "payment": (
                        "The payment attempt does not "
                        "belong to bKash."
                    ),
                    "provider": (
                        payment_attempt.provider
                    ),
                }
            )

        payment_id = (
            payment_attempt.provider_payment_id
        )

        if not payment_id:
            raise ValidationError(
                {
                    "payment": (
                        "bKash payment ID is missing."
                    )
                }
            )

        payment = payment_attempt.payment

        if payment.status != payment.Status.PENDING:
            raise ValidationError(
                {
                    "payment": (
                        "The payment is not pending."
                    ),
                    "payment_status": payment.status,
                }
            )

        if (
            payment_attempt.status
            != payment_attempt.Status.PENDING
        ):
            raise ValidationError(
                {
                    "payment": (
                        "The payment attempt is not pending."
                    ),
                    "payment_attempt_status": (
                        payment_attempt.status
                    ),
                }
            )

    # =============================================================
    # Execute Result
    # =============================================================

    @classmethod
    def _build_success_result(
        cls,
        result,
    ):
        transaction_id = result.get(
            "trx_id"
        )

        if not transaction_id:
            raise ValidationError(
                {
                    "payment": (
                        "bKash execution completed but "
                        "no transaction ID was returned."
                    )
                }
            )

        return {
            "status": "success",
            "transaction_id": transaction_id,
            "provider_response": result,
        }

    # =============================================================
    # Query Fallback
    # =============================================================

    @classmethod
    def _query_payment(
        cls,
        payment_id,
    ):
        result = (
            BkashPaymentQueryService.query_payment(
                payment_id=payment_id,
            )
        )

        transaction_status = result.get(
            "transaction_status"
        )

        transaction_id = result.get(
            "trx_id"
        )

        # ---------------------------------------------------------
        # Completed
        # ---------------------------------------------------------

        if transaction_status == cls.COMPLETED_STATUS:

            if not transaction_id:
                raise ValidationError(
                    {
                        "payment": (
                            "bKash reported the payment as "
                            "completed but did not return "
                            "a transaction ID."
                        ),
                        "payment_id": payment_id,
                    }
                )

            return {
                "status": "success",
                "transaction_id": transaction_id,
                "provider_response": result,
            }

        # ---------------------------------------------------------
        # Still Initiated
        # ---------------------------------------------------------

        if transaction_status == cls.INITIATED_STATUS:

            return {
                "status": "pending",
                "transaction_id": transaction_id,
                "provider_response": result,
            }

        # ---------------------------------------------------------
        # Terminal Failure
        # ---------------------------------------------------------

        if transaction_status in cls.FAILED_STATUSES:

            return {
                "status": "failed",
                "transaction_id": transaction_id,
                "provider_response": result,
            }

        # ---------------------------------------------------------
        # Unknown Status
        # ---------------------------------------------------------

        logger.error(
            "bKash returned an unexpected transaction status "
            "during reconciliation. payment_id=%s status=%s",
            payment_id,
            transaction_status,
        )

        raise ValidationError(
            {
                "payment": (
                    "bKash returned an unknown "
                    "transaction status."
                ),
                "payment_id": payment_id,
                "transaction_status": transaction_status,
            }
        )