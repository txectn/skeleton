from rest_framework import serializers

from .models import (
    Blog,
    BlogMedia,
    BlogComment,
    BlogLike,
    BlogCommentLike,
)

# ==========================================
# Blog Serializers
# ==========================================

class BlogSerializer(serializers.ModelSerializer):
    """
    Create and update blog posts.
    """

    class Meta:
        model = Blog

        fields = "__all__"

        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )

class BlogListSerializer(serializers.ModelSerializer):
    """
    Blog listing.
    Requires likes_count and comments_count annotations
    in the queryset.
    """

    likes_count = serializers.IntegerField(read_only=True)

    comments_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Blog

        fields = (
            "id",
            "name",
            "slug",
            "image",
            "short_description",
            "link",
            "likes_count",
            "comments_count",
            "published_at",
        )

        read_only_fields = fields

class BlogDetailSerializer(serializers.ModelSerializer):
    """
    Complete blog details with associated media.
    """

    media = serializers.SerializerMethodField()

    likes_count = serializers.IntegerField(read_only=True)

    comments_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Blog

        fields = (
            "id",
            "name",
            "slug",
            "image",
            "link",
            "short_description",
            "content",
            "meta_title",
            "meta_description",
            "likes_count",
            "comments_count",
            "published_at",
            "media",
            "created_at",
            "updated_at",
        )

        read_only_fields = fields

    def get_media(self, obj):
        return BlogMediaSerializer(
            obj.media.all(),
            many=True,
            context=self.context,
        ).data

# ==========================================
# Blog Media Serializer
# ==========================================

class BlogMediaSerializer(serializers.ModelSerializer):

    class Meta:
        model = BlogMedia

        fields = (
            "id",
            "file",
            "position",
            "created_at",
        )

        read_only_fields = (
            "id",
            "created_at",
        )

# ==========================================
# Blog Comment Serializer
# ==========================================

class BlogCommentSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        source="user.username",
        read_only=True,
    )

    class Meta:
        model = BlogComment

        fields = (
            "id",
            "blog",
            "user",
            "username",
            "content",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "user",
            "username",
            "created_at",
            "updated_at",
        )

# ==========================================
# Blog Like Serializer
# ==========================================

class BlogLikeSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        source="user.username",
        read_only=True,
    )

    class Meta:
        model = BlogLike

        fields = (
            "id",
            "blog",
            "user",
            "username",
            "created_at",
        )

        read_only_fields = (
            "id",
            "user",
            "username",
            "created_at",
        )

# ==========================================
# Blog Comment Like Serializer
# ==========================================

class BlogCommentLikeSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        source="user.username",
        read_only=True,
    )

    class Meta:
        model = BlogCommentLike

        fields = (
            "id",
            "comment",
            "user",
            "username",
            "created_at",
        )

        read_only_fields = (
            "id",
            "user",
            "username",
            "created_at",
        )