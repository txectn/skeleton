from rest_framework import serializers

from ..models import Product, Variant

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


class ProductListVariantSerializer(serializers.ModelSerializer):

    code = serializers.CharField(
        source="currency.code",
        read_only=True,
    )

    symbol = serializers.CharField(
        source="currency.symbol",
        read_only=True,
    )

    class Meta:
        model = Variant
        fields = [
            "id",
            "price",
            "code",
            "symbol",
        ]
        read_only_fields = [
            "id",
        ]

class ProductListSerializer(serializers.ModelSerializer):

    media = MediaSerializer(
        many=True,
        read_only=True,
    )

    variant = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "media",
            "variant",
            "is_active",
        ]
        read_only_fields = [
            "id",
        ]

    def get_variant(self, obj):
        variant = (
            obj.variants
            .filter(is_active=True)
            .order_by("position")
            .first()
        )

        if not variant:
            return None

        return ProductListVariantSerializer(
            variant,
            context=self.context,
        ).data

