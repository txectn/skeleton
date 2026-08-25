from rest_framework import serializers

from ..models import Product

from .media import MediaSerializer
from .brand import BrandSerializer
from .model import ModelSerializer
from .category import CategorySerializer
from .collection import CollectionSerializer
from .tag import TagSerializer
from .shippingClass import ShippingClassSerializer
from .option import OptionSerializer
from .variant import VariantSerializer
from .metafield import MetafieldSerializer

class ProductDetailSerializer(serializers.ModelSerializer):

    media = MediaSerializer(
        many=True,
        read_only=True,
    )

    brand = BrandSerializer(
        read_only=True,
    )

    model = ModelSerializer(
        read_only=True,
    )

    category = CategorySerializer(
        read_only=True,
    )

    collections = CollectionSerializer(
        many=True,
        read_only=True,
    )

    tags = TagSerializer(
        many=True,
        read_only=True,
    )

    shipping_class = ShippingClassSerializer(
        read_only=True,
    )

    options = OptionSerializer(
        many=True,
        read_only=True,
    )

    variants = VariantSerializer(
        many=True,
        read_only=True,
    )

    metafields = MetafieldSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "description",

            # Have Relation
            "media",
            "brand",
            "model",            
            "category",
            
            "collections",
            "tags",

            "shipping_class",

            "metafields",

            "options",
            "variants",

            # No Relation
            "is_active",
        ]
        read_only_fields = [
            "id",
        ]

class ProductListSerializer(serializers.ModelSerializer):

    media = MediaSerializer(
        many=True,
        read_only=True,
    )

    price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "media",
            "price",
            "is_active",
        ]
        read_only_fields = [
            "id",
        ]

    def get_price(self, obj):
        variant = (
            obj.variants
            .filter(is_active=True)
            .order_by("position")
            .first()
        )

        return variant.price if variant else None