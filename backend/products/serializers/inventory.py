from rest_framework import serializers

from ..models import Inventory

class InventorySerializer(serializers.ModelSerializer):
    # available_quantity = serializers.IntegerField(
    #     read_only=True,
    # )

    in_stock = serializers.SerializerMethodField()

    class Meta:
        model = Inventory
        fields = [
            "id",
            # "available_quantity",
            "in_stock",
        ]
        read_only_fields = [
            "id",
            # "available_quantity",
            "in_stock",
        ]

    def get_in_stock(self, obj):
        return obj.available_quantity > 0