from rest_framework import serializers

from ..models import Order

class OrderCancelSerializer(serializers.Serializer):

    order = serializers.PrimaryKeyRelatedField(
        queryset=Order.objects.all(),
    )