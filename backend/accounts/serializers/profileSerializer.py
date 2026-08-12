from rest_framework import serializers

from ..models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    username = serializers.CharField(source="user.username")

    class Meta:
        model = Profile
        fields = (
            "username",
            "first_name",
            "last_name",
            "avatar",
            "phone_number",
            "date_of_birth",
            "gender",
            "address",
            "city",
            "country",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "created_at",
            "updated_at",
        )

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", {})

        user = instance.user
        user.first_name = user_data.get("first_name", user.first_name)
        user.last_name = user_data.get("last_name", user.last_name)
        user.save(update_fields=["first_name", "last_name"])

        return super().update(instance, validated_data)