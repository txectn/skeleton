from django.urls import path

from .views import (
    AuthView, 
    ProfileView, 
    AuthVerifyRequestView, 
    LogoutAllView,
    RefreshTokenView
)

urlpatterns = [
    path("auth/", AuthView.as_view(), name="auth"),
    path("auth/verify/", AuthVerifyRequestView.as_view(), name="auth-verify"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("logout-all/", LogoutAllView.as_view(), name="logout"),
    path("refresh/", RefreshTokenView.as_view(), name="refresh-token"),
]
