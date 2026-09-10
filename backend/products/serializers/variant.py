from rest_framework import serializers

from ..models import Variant

from offers.services import OfferService

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

    offer = serializers.SerializerMethodField()

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
            "offer",
            "position",
            "is_active",
        ]

        read_only_fields = [
            "id",
        ]

    def get_offer(self, variant):
        pricing = OfferService.get_variant_pricing(variant)

        offer = pricing["offer"]

        if offer is None:
            return None

        return {
            "id": offer.id,
            "name": offer.name,
            "description": offer.description,
            "discount_type": offer.discount_type,
            "discount_value": offer.discount_value,
            "original_price": pricing["original_price"],
            "discount_amount": pricing["discount_amount"],
            "final_price": pricing["final_price"],
            "priority": offer.priority,
            "starts_at": offer.starts_at,
            "ends_at": offer.ends_at,
        }