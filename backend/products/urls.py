from django.urls import path

from .views import (
    ProductListView,
    ProductDetailView,
    CategoryListView,
    BrandListView,
)

urlpatterns = [
    # Product
    path("products/", ProductListView.as_view(), name="product-list"),
    path("products/<slug:slug>/", ProductDetailView.as_view(), name="product-detail"),

    # Category
    path("categories/", CategoryListView.as_view(), name="category-list"),

    # Brand 
    path("brands/", BrandListView.as_view(), name="brand-list"),
]
