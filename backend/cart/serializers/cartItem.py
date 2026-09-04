from rest_framework import serializers

from ..models import CartItem

from products.serializers import (
    MediaSerializer,
    VariantSerializer,
)

class CartProductSerializer(serializers.Serializer):
    id = serializers.IntegerField(
        source="variant.product.id",
        read_only=True,
    )

    name = serializers.CharField(
        source="variant.product.name",
        read_only=True,
    )

    media = MediaSerializer(
        source="variant.product.media",
        many=True,
        read_only=True,
    )

    variant = VariantSerializer(
        read_only=True,
    )


class CartItemSerializer(serializers.ModelSerializer):
    product = CartProductSerializer(
        source="*",
        read_only=True,
    )

    class Meta:
        model = CartItem
        fields = [
            "id",
            "product",
            # "variant",
            "quantity",
        ]

        read_only_fields = [
            "id",
        ]