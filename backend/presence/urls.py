from django.urls import path

from .views import PresenceView

urlpatterns = [
    path("presence/", PresenceView.as_view(), name="presence"),
]