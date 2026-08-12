from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

class LogoutAllView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        user.token_version += 1
        user.save(update_fields=["token_version"])

        return Response({
            "success": True,
            "message": "Logged out from all devices successfully."
        })