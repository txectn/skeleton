from ..models import Presence

class PresenceMatchService:

    MATCH_THRESHOLD = 70

    WEIGHTS = {
        "device_id": 35,
        "user_agent": 20,
        "browser": 10,
        "browser_version": 5,
        "operating_system": 10,
        "os_version": 5,
        "device_type": 15,
    }

    @classmethod
    def match(cls, *, fingerprint, data):
        presence = Presence.objects.filter(
            fingerprint=fingerprint,
        ).first()

        if presence:
            return presence

        return cls._score_match(data=data)

    @classmethod
    def _score_match(cls, *, data):
        best_presence = None
        best_score = 0

        for presence in Presence.objects.all():
            score = cls._calculate_score(
                presence=presence,
                data=data,
            )

            if score > best_score:
                best_score = score
                best_presence = presence

        if best_score >= cls.MATCH_THRESHOLD:
            return best_presence

        return None

    @classmethod
    def _calculate_score(cls, *, presence, data):
        score = 0

        fields = (
            "device_id",
            "user_agent",
            "browser",
            "browser_version",
            "operating_system",
            "os_version",
            "device_type",
        )

        for field in fields:
            current_value = data.get(field)
            stored_value = getattr(presence, field, None)

            if (
                current_value
                and stored_value
                and current_value == stored_value
            ):
                score += cls.WEIGHTS[field]

        return score