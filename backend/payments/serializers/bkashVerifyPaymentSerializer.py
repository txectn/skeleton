from rest_framework import serializers

class BkashVerifyPaymentSerializer(serializers.Serializer):

    paymentID = serializers.CharField(
        required=True,
        allow_blank=False,
        trim_whitespace=True,
    )

    status = serializers.CharField(
        required=True,
        allow_blank=False,
        trim_whitespace=True,
    )