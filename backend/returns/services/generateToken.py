
from datetime import timedelta

from django.db import transaction
from django.utils import timezone

from returns.models import ReturnRequest, ReturnActionToken

TOKEN_LIFETIME = timedelta(hours=24)

@transaction.atomic
def generate_return_action_token(return_request):
    """
    Generate a new action token for a specific return request.

    - Rejects unsaved or finished return requests.
    - Invalidates previous valid, unused tokens.
    - Creates a token that expires after 24 hours.
    - Returns the created ReturnActionToken instance.
    """

    if not return_request.pk:
        raise ValueError(
            "A saved return request is required."
        )

    return_request = (
        ReturnRequest.objects
        .select_for_update()
        .get(pk=return_request.pk)
    )

    terminal_statuses = {
        ReturnRequest.Status.COMPLETED,
        ReturnRequest.Status.FAILED,
        ReturnRequest.Status.CANCELLED,
    }

    if return_request.status in terminal_statuses:
        raise ValueError(
            "Cannot generate a token for a finished return request."
        )

    now = timezone.now()

    # Invalidate previous valid, unused tokens.
    ReturnActionToken.objects.filter(
        return_request=return_request,
        used_at__isnull=True,
        expires_at__gt=now,
    ).update(used_at=now)

    return ReturnActionToken.objects.create(
        return_request=return_request,
        expires_at=now + TOKEN_LIFETIME,
    )
