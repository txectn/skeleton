from ipware import get_client_ip
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import PresenceSerializer
from ..tasks import resolve_presence

class PresenceView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = PresenceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        client_ip, _ = get_client_ip(request)

        user_id = (
            request.user.id
            if request.user.is_authenticated
            else None
        )

        resolve_presence.delay(
            presence_id=serializer.validated_data.get("presence_id"),
            user_id=user_id,
            device_id=serializer.validated_data["device_id"],
            fingerprint=serializer.validated_data["fingerprint"],
            ip_address=client_ip,
            user_agent=serializer.validated_data.get("user_agent", ""),
            browser=serializer.validated_data.get("browser", ""),
            browser_version=serializer.validated_data.get(
                "browser_version", ""
            ),
            operating_system=serializer.validated_data.get(
                "operating_system", ""
            ),
            os_version=serializer.validated_data.get(
                "os_version", ""
            ),
            device_type=serializer.validated_data.get(
                "device_type", ""
            ),
        )

        return Response(
            {"detail": "Presence recorded."},
            status=status.HTTP_202_ACCEPTED,
        )