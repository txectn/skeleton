from rest_framework import serializers

from ..models import Model

class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = [
            "id",
            "brand",
            "name",
            "slug",
        ]
        read_only_fields = [
            "id",
        ]