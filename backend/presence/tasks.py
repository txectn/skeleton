import uuid

from celery import shared_task
from django.utils import timezone

from .models import Presence

@shared_task
def resolve_presence(
    presence_id,
    user_id,
    device_id,
    fingerprint,
    ip_address,
    user_agent="",
    browser="",
    browser_version="",
    operating_system="",
    os_version="",
    device_type="",
):
    """
    Find an existing presence or create a new one.

    user_id:
        Authenticated user's ID, or None for guests.

    presence_id:
        Client's persistent presence identifier.
    """

    now = timezone.now()

    presence = Presence.objects.filter(
        presence_id=presence_id
    ).first()

    if presence:
        presence.user_id = user_id
        presence.ip_address = ip_address
        presence.user_agent = user_agent
        presence.browser = browser
        presence.browser_version = browser_version
        presence.operating_system = operating_system
        presence.os_version = os_version
        presence.device_type = device_type
        presence.last_seen_at = now

        presence.save(
            update_fields=[
                "user",
                "ip_address",
                "user_agent",
                "browser",
                "browser_version",
                "operating_system",
                "os_version",
                "device_type",
                "last_seen_at",
            ]
        )

        return presence.id

    presence = Presence.objects.create(
        presence_id=presence_id or uuid.uuid4().hex,
        user_id=user_id,
        device_id=device_id,
        fingerprint=fingerprint,
        ip_address=ip_address,
        user_agent=user_agent,
        browser=browser,
        browser_version=browser_version,
        operating_system=operating_system,
        os_version=os_version,
        device_type=device_type,
    )

    return presence.id