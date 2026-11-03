from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import ReturnActionToken

from ..serializers import TokenSerializer, ReturnActionSerializer

from ..services import ReturnActionService

class ReturnTokenActionView(APIView):

    permission_classes = []

    def get(self, request, token):
        serializer = TokenSerializer(data={"token": token})
        serializer.is_valid(raise_exception=True)

        validated_token = serializer.validated_data["token"]

        result = ReturnActionService.get_Return_Data(validated_token)

        return Response(
            result,
            status=status.HTTP_200_OK
        )

    def patch(self, request, token):
        token_serializer = TokenSerializer(data={"token": token})
        token_serializer.is_valid(raise_exception=True)

        action_serializer = ReturnActionSerializer(data=request.data)
        action_serializer.is_valid(raise_exception=True)

        result = ReturnActionService.update_Return_Request(
            token=token_serializer.validated_data["token"],
            data=action_serializer.validated_data
        )

        return Response(
            result,
            status=status.HTTP_200_OK
        )
