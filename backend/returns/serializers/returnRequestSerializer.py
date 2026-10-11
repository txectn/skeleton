from rest_framework import serializers

from ..models import ReturnRequest

class ReturnRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReturnRequest
        fields = [
            "order",
            "reason",
            "customer_note",
        ]

        read_only_fields = [
            "status",
            "decision",
            "inspector_note",
            "return_charge",
            "refund_amount",
            "created_at",
            "updated_at",
        ]