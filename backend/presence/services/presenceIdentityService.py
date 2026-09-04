from ..models import Presence
from .fingerprintService import FingerprintService
from .presenceMatchService import PresenceMatchService

class PresenceIdentityService:

    @staticmethod
    def resolve(*, data):
        presence_id = data.get("presence_id")

        if presence_id:
            presence = Presence.objects.filter(
                presence_id=presence_id,
            ).first()

            if presence:
                return presence.presence_id

        fingerprint = FingerprintService.create(
            data=data,
        )

        presence = PresenceMatchService.match(
            fingerprint=fingerprint,
            data={
                **data,
                "fingerprint": fingerprint,
            },
        )

        if presence:
            return presence.presence_id

        return None