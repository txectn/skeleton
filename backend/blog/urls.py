from django.urls import path

from .views import (
    BlogListView,
    BlogDetailView,
    BlogCommentListCreateView,
    BlogCommentDetailView,
    BlogLikeView,
    BlogCommentLikeView,
)

urlpatterns = [
    # Blog
    path("blogs/", BlogListView.as_view(), name="blog-list"),

    path("blogs/<slug:slug>/", BlogDetailView.as_view(), name="blog-detail"),

    # Blog Comments
    path("blogs/<slug:slug>/comments/", BlogCommentListCreateView.as_view(), name="blog-comment-list-create"),

    path("blog-comments/<int:pk>/", BlogCommentDetailView.as_view(), name="blog-comment-detail"),

    # Blog Likes
    path("blogs/<slug:slug>/like/", BlogLikeView.as_view(), name="blog-like"),

    # Blog Comment Likes
    path("blog-comments/<int:pk>/like/", BlogCommentLikeView.as_view(), name="blog-comment-like"),

]