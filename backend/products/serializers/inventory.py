from rest_framework import serializers

from ..models import Inventory

class InventorySerializer(serializers.ModelSerializer):
    available_quantity = serializers.IntegerField(
        read_only=True,
    )

    class Meta:
        model = Inventory
        fields = [
            "id",
            "available_quantity",
        ]
        read_only_fields = [
            "id",
            "available_quantity",
        ]

    def validate(self, attrs):
        quantity = attrs.get(
            "quantity",
            self.instance.quantity if self.instance else 0,
        )

        reserved_quantity = attrs.get(
            "reserved_quantity",
            self.instance.reserved_quantity if self.instance else 0,
        )

        if reserved_quantity > quantity:
            raise serializers.ValidationError(
                {
                    "reserved_quantity": (
                        "Reserved quantity cannot be greater than total quantity."
                    )
                }
            )

        return attrs