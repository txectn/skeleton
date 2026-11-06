from rest_framework import serializers

from .models import (
    Banner
)

class BannerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Banner

        fields = (
            "id",
            "title",
            "heading",
            "subtitle",
            "image",
            "mobile_image",
            "destination_type",
            "collection",
            "promotion",
            "product",
            "custom_url",
            "cta_label",
            "position",
            "starts_at",
            "ends_at",
            "is_active",
        )

        read_only_fields = fields