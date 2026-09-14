from rest_framework import serializers

from ..models import Variant

from promotions.services import PromotionResponseService

from .option import OptionSerializer
from .inventory import InventorySerializer
from .currency import CurrencySerializer

class VariantSerializer(serializers.ModelSerializer):

    options = OptionSerializer(
        many=True,
        read_only=True,
    )

    inventory = InventorySerializer(
        read_only=True,
    )

    currency = CurrencySerializer(
        read_only=True,
    )

    promotion = serializers.SerializerMethodField()

    class Meta:
        model = Variant

        fields = [
            "id",
            "sku",
            "price",
            "compare_at_price",
            "options",
            "inventory",
            "currency",
            "promotion",
            "position",
            "is_active",
        ]

        read_only_fields = [
            "id",
        ]

    def get_promotion(self, variant):
        return PromotionResponseService.get_promotion(variant)
