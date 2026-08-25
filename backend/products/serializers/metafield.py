from rest_framework import serializers

from ..models import Metafield

class MetafieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metafield
        fields = [
            "id",
            "product",
            "namespace",
            "key",
            "value",
        ]
        read_only_fields = [
            "id",
        ]