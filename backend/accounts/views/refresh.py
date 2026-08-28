from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from ..services import RefreshTokenService

class RefreshTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        result = RefreshTokenService.refresh(
            request.data.get("refresh")
        )

        return Response(result)