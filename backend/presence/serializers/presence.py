from rest_framework import serializers

from ..models import Presence

class PresenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Presence

        fields = (
            "presence_id",
            "device_id",
            "fingerprint",
            "user_agent",
            "browser",
            "browser_version",
            "operating_system",
            "os_version",
            "device_type",
        )

        extra_kwargs = {
            "presence_id": {
                "required": False,
                "allow_blank": True,
                "validators": [],
            },
            "device_id": {
                "required": True,
            },
            "fingerprint": {
                "required": False,
                "allow_blank": True,
            },
            "user_agent": {
                "required": False,
                "allow_blank": True,
            },
            "browser": {
                "required": False,
                "allow_blank": True,
            },
            "browser_version": {
                "required": False,
                "allow_blank": True,
            },
            "operating_system": {
                "required": False,
                "allow_blank": True,
            },
            "os_version": {
                "required": False,
                "allow_blank": True,
            },
            "device_type": {
                "required": False,
                "allow_blank": True,
            },
        }