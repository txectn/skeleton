from rest_framework.views import APIView
from rest_framework.response import Response

from ..services import QuantityValidator
from ..serializers import QuantityValidatorSerializer

class QuantityValidatorView(APIView):
    permission_classes = []
    serializer_class = QuantityValidatorSerializer

    def post(self, request):
        serializer = QuantityValidatorSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        return Response(
            QuantityValidator.validate(
                **serializer.validated_data,
            )
        )