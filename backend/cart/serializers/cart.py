from rest_framework import serializers

from ..models import Cart

from .cartItem import CartItemSerializer

class CartSerializer(serializers.ModelSerializer):

    items = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = [
            "id",
            "items",
        ]

        read_only_fields = [
            "id",
        ]

    def get_items(self, cart):
        items = self.context.get(
            "items",
            cart.items.all(),
        )

        return CartItemSerializer(
            items,
            many=True,
            context=self.context,
        ).data