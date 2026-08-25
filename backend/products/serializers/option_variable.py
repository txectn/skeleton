from rest_framework import serializers

from ..models import OptionVariable

class OptionVariableSerializer(serializers.ModelSerializer):
    class Meta:
        model = OptionVariable
        fields = [
            "id",
            "name",
        ]
        read_only_fields = [
            "id",
        ]