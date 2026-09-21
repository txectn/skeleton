from rest_framework import serializers

from products.models import Variant

class OrderSerializer(serializers.Serializer):

    variant = serializers.PrimaryKeyRelatedField(
        queryset=Variant.objects.all(),
    )

    quantity = serializers.IntegerField(
        min_value=1,
    )
