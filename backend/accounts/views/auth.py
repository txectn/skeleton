from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import SocialLoginSerializer
from ..services.authService import AuthService


class AuthView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = SocialLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = AuthService.login(request=request, **serializer.validated_data)
        return Response(
            result,
            # result["data"],
            # status=result.get("status", status.HTTP_200_OK),
        )


# Flow
# Login with any provider.
# Determine the authentication provider from the serializer data.
# Verify the provider token and email.
# Check if the user exists; create if not.
# Create JWT tokens.
# Store the refresh token and device data in the user session.
# Create a login history record.
# Return the JWT tokens.
