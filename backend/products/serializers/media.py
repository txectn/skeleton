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

    def to_representation(self, instance):
        data = super().to_representation(instance)

        file_url = data.pop("file", None)

        if instance.media_type == "image":
            data["image"] = file_url

        elif instance.media_type == "video":
            data["video"] = file_url

        else:
            data["file"] = file_url

        return data