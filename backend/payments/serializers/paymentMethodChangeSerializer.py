from rest_framework import serializers

from orders.models import Order
from ..models import Payment

class PaymentMethodChangeSerializer(serializers.Serializer):

    order = serializers.PrimaryKeyRelatedField(
        queryset=Order.objects.all(),
    )

    payment_method = serializers.ChoiceField(
        choices=Payment.Method.choices,
    )

    provider = serializers.CharField(
        required=False,
        allow_blank=True,
    )