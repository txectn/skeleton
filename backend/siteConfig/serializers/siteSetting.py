from rest_framework import serializers
from ..models import SiteSetting

class SiteSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSetting
        fields = [
            "id",
            "site_name",
            "logo",
            "favicon",
            "email",
            "phone_number",
            "address",
            "timezone",
            "updated_at",
        ]
        read_only_fields = ["id", "updated_at"]