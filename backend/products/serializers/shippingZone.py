from rest_framework import serializers

from ..models.shippingZone import ShippingZone

class ShippingZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingZone
        fields = [
            "id",
            "name",
            "country",
            "region",
            "city",
        ]