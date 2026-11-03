from django.db import models
from django.utils import timezone
from django.conf import settings
from django.core.validators import FileExtensionValidator

class Blog(models.Model):

    name = models.CharField(max_length=255)

    slug = models.SlugField(
        max_length=255,
        unique=True,
    )

    image = models.ImageField(
        upload_to="blogs/"
    )

    link = models.URLField(
        blank=True,
        null=True,
    )

    short_description = models.TextField()

    content = models.TextField()

    meta_title = models.CharField(
        max_length=255,
        blank=True,
    )

    meta_description = models.TextField(
        blank=True,
    )

    is_published = models.BooleanField(default=False)

    published_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):

        if self.is_published and not self.published_at:
            self.published_at = timezone.now()

        elif not self.is_published:
            self.published_at = None

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class BlogMedia(models.Model):

    blog = models.ForeignKey(
        Blog,
        on_delete=models.CASCADE,
        related_name="media",
    )

    file = models.FileField(
        upload_to="blogs/media/",
        validators=[
            FileExtensionValidator(
                allowed_extensions=[
                    # Images
                    "jpg",
                    "jpeg",
                    "png",
                    "webp",
                    "gif",

                    # Videos
                    "mp4",
                    "webm",
                    "mov",
                ]
            )
        ],
    )

    position = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("position",)

        constraints = [
            models.UniqueConstraint(
                fields=("blog", "position"),
                name="unique_blog_media_position",
            ),
        ]

    def __str__(self):
        return f"{self.blog.name} - Media {self.id}"

class BlogComment(models.Model):

    blog = models.ForeignKey(
        Blog,
        on_delete=models.CASCADE,
        related_name="comments",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="blog_comments",
    )

    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.user} - {self.blog.name}"

class BlogLike(models.Model):

    blog = models.ForeignKey(
        Blog,
        on_delete=models.CASCADE,
        related_name="likes",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="blog_likes",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("blog", "user"),
                name="unique_user_blog_like",
            ),
        ]

    def __str__(self):
        return f"{self.user} liked {self.blog.name}"

class BlogCommentLike(models.Model):

    comment = models.ForeignKey(
        BlogComment,
        on_delete=models.CASCADE,
        related_name="likes",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="blog_comment_likes",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("comment", "user"),
                name="unique_user_blog_comment_like",
            ),
        ]

    def __str__(self):
        return f"{self.user} liked comment {self.comment_id}"