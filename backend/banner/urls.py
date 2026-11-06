from django.urls import path

from .views import BannerListView


urlpatterns = [
    path("banner/", BannerListView.as_view(), name="banner-list"),
]