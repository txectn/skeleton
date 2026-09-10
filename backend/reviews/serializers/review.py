from rest_framework import serializers

from ..models import Review

class ReviewSerializer(serializers.ModelSerializer):
    # user = serializers.CharField(source="user.username", read_only=True)
    user = serializers.SerializerMethodField()
    like_count = serializers.IntegerField(read_only=True)
    is_liked = serializers.BooleanField(read_only=True)

    class Meta:
        model = Review

        fields = [
            "id",
            "user",
            "product",
            "rating",
            "title",
            "message",
            "like_count",
            "is_liked",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "user",
            "product",
            "rating",
            "title",
            "message",
            "like_count",
            "is_liked",
            "created_at",
        ]

    def get_user(self, obj):
        user = obj.user

        if user.first_name or user.last_name:
            return " ".join(
                name
                for name in [user.first_name, user.last_name]
                if name
            )

        return user.username