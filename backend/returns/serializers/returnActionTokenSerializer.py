from rest_framework import serializers

from ..models import ReturnRequest, ReturnActionToken

class TokenSerializer(serializers.Serializer):
    token = serializers.UUIDField(
        required=True,
        allow_null=False,
    )

class ReturnActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReturnRequest
        fields = [
            "status",
            "decision",
            "inspector_note",
            "customer_note",
        ]

        read_only_fields = [
            "id",
            "customer_note",
        ]