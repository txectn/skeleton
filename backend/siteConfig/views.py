from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from common.permissions import IsAdmin
from .models import SiteSetting
from .serializers import SiteSettingSerializer

class SiteSettingDetailView(APIView):
    """
    Get, create, or update global site settings.
    - Read (GET): Public access
    - Create/Update (POST/PUT/PATCH): Admin only
    """

    def get_permissions(self):
        # Allow anyone to read, require IsAdmin for modifying operations

        if self.request.method in ["POST", "PUT", "PATCH"]:
            return [IsAdmin()]
        
        return [AllowAny()]

    def get_object(self):
        # Returns the existing setting instance or None if not created yet

        return SiteSetting.objects.first()

    def get(self, request):
        setting = self.get_object()

        if not setting:
            return Response(
                {"detail": "Site settings have not been configured yet."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = SiteSettingSerializer(setting, context={"request": request})

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if self.get_object():
            return Response(
                {"detail": "Site settings already exist. Use PUT or PATCH to update."},
                status=status.HTTP_400_BAD_REQUEST,
            )
            
        serializer = SiteSettingSerializer(data=request.data, context={"request": request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        return self._update(request, partial=False)

    def patch(self, request):
        return self._update(request, partial=True)

    def _update(self, request, partial=False):
        setting = self.get_object()

        if not setting:
            return Response(
                {"detail": "Site settings do not exist yet. Create them first with POST."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = SiteSettingSerializer(
            setting, data=request.data, partial=partial, context={"request": request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)