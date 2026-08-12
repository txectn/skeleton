from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated

from ..models import Profile
from ..serializers import ProfileSerializer

class ProfileView(RetrieveUpdateAPIView):
    """
    Retrieve and update the authenticated user's profile.
    """

    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "patch", "put"]

    def get_object(self):
        profile, _ = Profile.objects.select_related("user").get_or_create(
            user=self.request.user,
        )

        return profile