from rest_framework import serializers

class CartClearSerializer(serializers.Serializer):
    cart_token = serializers.UUIDField(
        required=False,
        allow_null=True,
    )