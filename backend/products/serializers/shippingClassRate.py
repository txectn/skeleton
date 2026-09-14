from rest_framework import serializers

from ..models.shippingClassRate import ShippingClassRate

from .shippingZone import ShippingZoneSerializer
from .shippingClass import ShippingClassSerializer

class ShippingClassRateSerializer(serializers.ModelSerializer):
    shipping_zone = ShippingZoneSerializer(
        read_only=True
    )
    shipping_class = ShippingClassSerializer(
        read_only=True
    )
    class Meta:
        model = ShippingClassRate
        fields = [
            "id",
            "shipping_class",
            "shipping_zone",
            "inner_zone_rate",
            "outer_zone_rate",
            "flat_rate",
        ]
        
        read_only_fields = [
            "id",
            "inner_zone_rate",
            "outer_zone_rate",
            "flat_rate",
        ]