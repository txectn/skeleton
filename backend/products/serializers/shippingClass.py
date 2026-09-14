from rest_framework import serializers

from ..models import ShippingClass

class ShippingClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingClass
        fields = [
            "id",
            "name",
        ]
        read_only_fields = [
            "id",
        ]