from rest_framework.response import Response
from rest_framework.views import APIView

from ...permissions import IsStaffOrSuperUser
from ...services import UserSummaryService

class UserSummaryView(APIView):
    # permission_classes = [IsStaffOrSuperUser]
    permission_classes = []

    def get(self, request):
        data = UserSummaryService.get_summary()

        return Response(data)