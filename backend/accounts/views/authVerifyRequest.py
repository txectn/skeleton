from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

class AuthVerifyRequestView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        return Response({"success": True})