from rest_framework import serializers

from ..models import ReturnRequest

class ReturnRequestCancelSerializer(serializers.Serializer):

    return_request = serializers.PrimaryKeyRelatedField(
        queryset=ReturnRequest.objects.all(),
    )