from django.db.models import Count
from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)

from rest_framework.generics import GenericAPIView

from .models import (
    Blog,
    BlogComment,
    BlogLike,
    BlogCommentLike,
)

from .serializers import (
    BlogListSerializer,
    BlogDetailSerializer,
    BlogCommentSerializer,
    BlogLikeSerializer,
    BlogCommentLikeSerializer,
)

from .pagination import (
    BlogCursorPagination,
    BlogCommentCursorPagination
)

# ==========================================
# Blog Views (Read Only)
# ==========================================

class BlogListView(generics.ListAPIView):

    serializer_class = BlogListSerializer
    permission_classes = [AllowAny]
    pagination_class = BlogCursorPagination

    def get_queryset(self):

        return Blog.objects.filter(
            is_published=True,
        ).annotate(
            likes_count=Count("likes", distinct=True),
            comments_count=Count("comments", distinct=True),
        )

class BlogDetailView(generics.RetrieveAPIView):

    serializer_class = BlogDetailSerializer
    permission_classes = [AllowAny]
    lookup_field = "slug"

    def get_queryset(self):

        return Blog.objects.filter(
            is_published=True,
        ).annotate(
            likes_count=Count("likes", distinct=True),
            comments_count=Count("comments", distinct=True),
        ).prefetch_related("media")

# ==========================================
# Blog Comment Views
# ==========================================

class BlogCommentListCreateView(generics.ListCreateAPIView):

    serializer_class = BlogCommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = BlogCommentCursorPagination

    def get_blog(self):

        return get_object_or_404(
            Blog,
            slug=self.kwargs["slug"],
            is_published=True,
        )

    def get_queryset(self):

        return BlogComment.objects.filter(
            blog=self.get_blog(),
        ).select_related("user")

    def perform_create(self, serializer):

        serializer.save(
            blog=self.get_blog(),
            user=self.request.user,
        )

class BlogCommentDetailView(
    generics.RetrieveUpdateDestroyAPIView
):

    serializer_class = BlogCommentSerializer
    permission_classes = [IsAuthenticated]

    http_method_names = ["get", "patch", "delete"]

    def get_queryset(self):

        return BlogComment.objects.filter(
            user=self.request.user,
        ).select_related("user")

# ==========================================
# Blog Like Views
# ==========================================

class BlogLikeView(GenericAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = BlogLikeSerializer

    def get_blog(self):

        return get_object_or_404(
            Blog,
            slug=self.kwargs["slug"],
            is_published=True,
        )

    def post(self, request, *args, **kwargs):

        blog = self.get_blog()

        like, created = BlogLike.objects.get_or_create(
            blog=blog,
            user=request.user,
        )

        serializer = self.get_serializer(like)

        return Response(
            serializer.data,
            status=(
                status.HTTP_201_CREATED
                if created
                else status.HTTP_200_OK
            ),
        )

    def delete(self, request, *args, **kwargs):

        blog = self.get_blog()

        BlogLike.objects.filter(
            blog=blog,
            user=request.user,
        ).delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )

# ==========================================
# Blog Comment Like Views
# ==========================================

class BlogCommentLikeView(GenericAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = BlogCommentLikeSerializer

    def get_comment(self):

        return get_object_or_404(
            BlogComment,
            pk=self.kwargs["pk"],
            blog__is_published=True,
        )

    def post(self, request, *args, **kwargs):

        comment = self.get_comment()

        like, created = BlogCommentLike.objects.get_or_create(
            comment=comment,
            user=request.user,
        )

        serializer = self.get_serializer(like)

        return Response(
            serializer.data,
            status=(
                status.HTTP_201_CREATED
                if created
                else status.HTTP_200_OK
            ),
        )

    def delete(self, request, *args, **kwargs):

        comment = self.get_comment()

        BlogCommentLike.objects.filter(
            comment=comment,
            user=request.user,
        ).delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )