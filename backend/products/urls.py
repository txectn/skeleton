from django.urls import path

from .views import (
    ProductListView,
    ProductDetailView,
    CategoryListView,
    BrandListView,
    CollectionListView,
    TagListView,
)

urlpatterns = [
    # Product
    path("products/", ProductListView.as_view(), name="product-list"),
    path("products/<slug:slug>/", ProductDetailView.as_view(), name="product-detail"),

    # Category
    path("categories/", CategoryListView.as_view(), name="category-list"),

    # Brand 
    path("brands/", BrandListView.as_view(), name="brand-list"),

    # Collection
    path("collections/", CollectionListView.as_view(), name="collection-list"),

    # Tag
    path("tags/", TagListView.as_view(), name="tag-list"),
]
