from rest_framework import serializers

from ..models import Media

class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = [
            "id",
            "file",
            "media_type",
            "alt_text",
            "position",
        ]
        read_only_fields = [
            "id",
        ]