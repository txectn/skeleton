from rest_framework import serializers

from products.serializers import (
    MediaSerializer,
    VariantSerializer,
)

class CheckoutProductSerializer(serializers.Serializer):
    id = serializers.IntegerField(
        source="cart_item.variant.product.id",
        read_only=True,
    )

    name = serializers.CharField(
        source="cart_item.variant.product.name",
        read_only=True,
    )

    media = MediaSerializer(
        source="cart_item.variant.product.media",
        many=True,
        read_only=True,
    )

    variant = VariantSerializer(
        source="cart_item.variant",
        read_only=True,
    )

class CheckoutShippingSerializer(serializers.Serializer):
    shipping_class = serializers.SerializerMethodField()

    rate = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True,
    )

    def get_shipping_class(self, obj):
        shipping_class = obj["shipping_class"]

        if shipping_class is None:
            return None

        return {
            "id": shipping_class.id,
            "name": shipping_class.name,
        }

class CheckoutItemSerializer(serializers.Serializer):
    id = serializers.IntegerField(
        source="cart_item.id",
        read_only=True,
    )

    product = CheckoutProductSerializer(
        source="*",
        read_only=True,
    )

    quantity = serializers.IntegerField(
        read_only=True,
    )

    shipping = CheckoutShippingSerializer(
        read_only=True,
    )

class CheckoutSerializer(serializers.Serializer):
    items = CheckoutItemSerializer(
        many=True,
        read_only=True,
    )
