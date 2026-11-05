from rest_framework import serializers

from .models import (
    AboutPage,
    AboutSection,
    AboutItem,
)

# =====================================
# About Item Serializer
# =====================================

class AboutItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = AboutItem

        fields = (
            "id",
            "title",
            "description",
            "icon",
        )

        read_only_fields = fields

# =====================================
# About Section Serializer
# =====================================

class AboutSectionSerializer(serializers.ModelSerializer):

    items = AboutItemSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = AboutSection

        fields = (
            "id",
            "section_id",
            "title",
            "heading",
            "description",
            "cta_link",
            "cta_label",
            "position",
            "image_position",
            "image",
            "items",
        )

        read_only_fields = fields

# =====================================
# About Page Serializer
# =====================================

class AboutPageSerializer(serializers.ModelSerializer):

    sections = AboutSectionSerializer(
        source="about_sections",
        many=True,
        read_only=True,
    )

    class Meta:
        model = AboutPage

        fields = (
            "id",
            "sections",
        )

        read_only_fields = fields