from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import ReturnRequestCancelSerializer
from ..services import ReturnRequestCancelService

class ReturnRequestCancelView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ReturnRequestCancelSerializer(
            data=request.data,
        )
        serializer.is_valid(
            raise_exception=True,
        )

        result = ReturnRequestCancelService.cancel(
            user=request.user,
            data=serializer.validated_data,
        )

        return Response(
            result,
            status=status.HTTP_200_OK,
        )