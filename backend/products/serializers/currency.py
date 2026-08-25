from rest_framework import serializers

from ..models import Currency

class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = [
            "id",
            "code",
            "name",
            "symbol",
        ]
        read_only_fields = [
            "id",
        ]