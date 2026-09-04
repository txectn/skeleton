from ipware import get_client_ip
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import PresenceSerializer
from ..tasks import resolve_presence
from ..services import (
    PresenceIdentityService,
)

class PresenceView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = PresenceSerializer(
            data=request.data,
        )
        serializer.is_valid(
            raise_exception=True,
        )

        data = serializer.validated_data

        presence_id = PresenceIdentityService.resolve(
            data=data,
        )

        if presence_id:
            data = {
                **data,
                "presence_id": presence_id,
            }

        resolve_presence.delay(
            data=data,
            user_id=(
                request.user.id
                if request.user.is_authenticated
                else None
            ),
            ip_address=get_client_ip(request)[0],
        )

        return Response({
            "detail": "Presence recorded.",
            "presence_id": presence_id,
        })
