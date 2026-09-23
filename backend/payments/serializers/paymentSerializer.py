from rest_framework import serializers

from orders.models import Order

class PaymentSerializer(serializers.Serializer):

    order = serializers.PrimaryKeyRelatedField(
        queryset=Order.objects.all(),
    )

    payment_method = serializers.CharField()