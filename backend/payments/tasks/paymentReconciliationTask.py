from celery import shared_task
from django.db import transaction

from payments.models import PaymentAttempt
from ..services import (
    PaymentReconciliationService,
)

@shared_task
def payment_reconciliation_task():

    payment_attempts = (
        PaymentAttempt.objects
        .select_related(
            "payment",
            "payment__order",
        )
        .filter(
            payment__method="online",
            payment__status="pending",
            status=PaymentAttempt.Status.PENDING,
        )
    )

    processed = 0
    failed = 0

    for payment_attempt in payment_attempts:

        try:

            with transaction.atomic():

                PaymentReconciliationService.reconcile(
                    payment_attempt=payment_attempt,
                )

            processed += 1

        except Exception:
            failed += 1

    return {
        "processed": processed,
        "failed": failed,
    }