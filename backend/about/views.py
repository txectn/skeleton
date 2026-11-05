from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import AboutPage
from .serializers import AboutPageSerializer

# =====================================
# About Page View
# =====================================

class AboutPageView(APIView):

    permission_classes = []

    def get(self, request):

        about_page = (
            AboutPage.objects
            .filter(is_active=True)
            .prefetch_related(
                "about_sections",
                "about_sections__items",
            )
            .first()
        )

        if not about_page:
            return Response(
                {
                    "detail": "About page not found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = AboutPageSerializer(about_page)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )