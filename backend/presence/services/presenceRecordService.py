from django.utils import timezone

from ..models import Presence

class PresenceRecordService:

    @staticmethod
    def record(
        *,
        presence=None,
        data,
        user=None,
        ip_address=None,
    ):
        if presence is None:
            return Presence.objects.create(
                user=user,
                device_id=data["device_id"],
                fingerprint=data["fingerprint"],
                ip_address=ip_address,
                user_agent=data.get("user_agent", ""),
                browser=data.get("browser", ""),
                browser_version=data.get(
                    "browser_version",
                    "",
                ),
                operating_system=data.get(
                    "operating_system",
                    "",
                ),
                os_version=data.get(
                    "os_version",
                    "",
                ),
                device_type=data.get(
                    "device_type",
                    "",
                ),
            )

        presence.user = user or presence.user
        presence.device_id = data["device_id"]
        presence.fingerprint = data.get(
            "fingerprint",
            presence.fingerprint,
        )
        presence.ip_address = ip_address
        presence.user_agent = data.get("user_agent", "")
        presence.browser = data.get("browser", "")
        presence.browser_version = data.get(
            "browser_version",
            "",
        )
        presence.operating_system = data.get(
            "operating_system",
            "",
        )
        presence.os_version = data.get(
            "os_version",
            "",
        )
        presence.device_type = data.get(
            "device_type",
            "",
        )
        presence.last_seen_at = timezone.now()

        presence.save()

        return presence