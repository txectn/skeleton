from rest_framework import generics
from rest_framework.permissions import AllowAny

from common.captcha import CaptchaMixin

from .models import ContactMessage
from .serializers import ContactMessageSerializer

from .throttles import ContactThrottle

class ContactMessageView(
    CaptchaMixin,
    generics.CreateAPIView,
):

    queryset = ContactMessage.objects.all()

    serializer_class = ContactMessageSerializer

    permission_classes = [AllowAny]

    captcha_scope = "contact_captcha"

    throttle_classes = [
        ContactThrottle,
    ]