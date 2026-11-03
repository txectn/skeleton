from django.urls import path
from .views import SiteSettingDetailView

urlpatterns = [
    path("site-settings/", SiteSettingDetailView.as_view(), name="site-setting"),
]