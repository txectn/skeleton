from rest_framework import serializers

from ..models import Option

class OptionSerializer(serializers.ModelSerializer):

    name = serializers.CharField(
        source="option_variable.name",
        read_only=True,
    )

    option_variable = serializers.IntegerField(
        source="option_variable.id",
        read_only=True,
    )

    class Meta:
        model = Option
        fields = [
            "id",
            "option_variable",
            "name",
            "value",
            "position",
        ]
        read_only_fields = [
            "id",
        ]