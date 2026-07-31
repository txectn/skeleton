from rest_framework import serializers

class DeviceInfoSerializer(serializers.Serializer):
    device = serializers.CharField(max_length=255)
    browser = serializers.CharField(max_length=255)
    operating_system = serializers.CharField(max_length=255)

class SocialLoginSerializer(serializers.Serializer):
    PROVIDER_CHOICES = (
        ("clerk", "Clerk"),
        ("google", "Google"),
        ("facebook", "Facebook"),
    )

    provider = serializers.ChoiceField(choices=PROVIDER_CHOICES)
    device = DeviceInfoSerializer()