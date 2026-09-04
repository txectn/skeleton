from ..models import Presence
from .fingerprintService import FingerprintService
from .presenceMatchService import PresenceMatchService

class PresenceResolveService:

    @staticmethod
    def resolve(
        *,
        data,
        user=None,
    ):
        if user:
            presence = Presence.objects.filter(
                user=user,
            ).first()

            if presence:
                return presence, data

        presence_id = data.get("presence_id")

        if presence_id:
            presence = Presence.objects.filter(
                presence_id=presence_id,
            ).first()

            if presence:
                return presence, data

        # fingerprint = data.get("fingerprint")

        # if fingerprint:
        #     presence = PresenceMatchService.match(
        #         fingerprint=fingerprint,
        #         data=data,
        #     )

        #     if presence:
        #         return presence, data

        fingerprint = FingerprintService.create(
            data=data,
        )

        data = {
            **data,
            "fingerprint": fingerprint,
        }

        presence = PresenceMatchService.match(
            fingerprint=fingerprint,
            data=data,
        )

        return presence, data