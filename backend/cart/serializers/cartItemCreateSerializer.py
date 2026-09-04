from rest_framework import serializers

from products.models import Variant

class CartItemCreateSerializer(serializers.Serializer):
    variant = serializers.PrimaryKeyRelatedField(
        queryset=Variant.objects.all(),
        error_messages={
            "required": "Product variant is required.",
            "null": "Product variant cannot be null.",
            "does_not_exist": "The selected product variant does not exist.",
            "incorrect_type": "Product variant must be a valid ID.",
        },
    )

    quantity = serializers.IntegerField(
        min_value=1,
    )

    cart_token = serializers.UUIDField(
        required=False,
        allow_null=True,
    )