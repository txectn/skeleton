from celery import shared_task
from django.contrib.auth import get_user_model

from .services import (
    PresenceResolveService,
    PresenceRecordService,
)

@shared_task
def resolve_presence(
    *,
    data,
    user_id=None,
    ip_address=None,
):
    User = get_user_model()

    user = None

    if user_id:
        user = User.objects.filter(
            id=user_id,
        ).first()

    presence, data = PresenceResolveService.resolve(
        data=data,
        user=user,
    )

    presence = PresenceRecordService.record(
        presence=presence,
        data=data,
        user=user,
        ip_address=ip_address,
    )

    return presence.id


# services/
# ├── presence_resolve_service.py
# ├── presence_record_service.py
# └── helpers/
#     ├── fingerprint_service.py
#     └── presence_match_service.py