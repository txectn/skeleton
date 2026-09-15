from rest_framework import serializers

from products.models import Variant

class QuantityValidatorSerializer(serializers.Serializer):
    variant = serializers.PrimaryKeyRelatedField(
        queryset=Variant.objects.filter(
            is_active=True,
        ),
    )
    quantity = serializers.IntegerField(
        min_value=1,
    )