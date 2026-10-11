from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..serializers import ReturnRequestSerializer
from ..services import ReturnRequestService

class ReturnRequestView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ReturnRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = ReturnRequestService.create(
            user=request.user,
            data=serializer.validated_data,
        )

        return Response(
            result,
            status=status.HTTP_201_CREATED,
        )