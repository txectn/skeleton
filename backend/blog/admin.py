from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from django.utils.html import format_html

from .models import (
    Blog,
    BlogMedia,
    BlogComment,
    BlogLike,
    BlogCommentLike,
)

# Blog Media Inline
class BlogMediaInline(TabularInline):

    model = BlogMedia

    extra = 1

    fields = (
        "file",
        "position",
        "created_at",
    )

    readonly_fields = (
        "created_at",
    )

    ordering = (
        "position",
    )

# Blog Admin
@admin.register(Blog)
class BlogAdmin(ModelAdmin):

    inlines = [
        BlogMediaInline,
    ]

    list_display = (
        "thumbnail_image",
        "id",
        "name",
        "is_published",
        "published_at",
        "created_at",
    )

    list_display_links = (
        "thumbnail_image",
        "id",
        "name",
    )

    list_filter = (
        "is_published",
        "published_at",
        "created_at",
    )

    search_fields = (
        "name",
        "short_description",
        "content",
        "meta_title",
    )

    prepopulated_fields = {
        "slug": ("name",),
    }

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    list_per_page = 20

    fieldsets = (
        ("Blog Information", {
            "fields": (
                "name",
                "slug",
                "image",
                "link",
                "short_description",
                "content",
            ),
        }),
        ("SEO Settings", {
            "fields": (
                "meta_title",
                "meta_description",
            ),
        }),
        ("Publishing", {
            "fields": (
                "is_published",
                "published_at",
            ),
        }),
        ("Timestamps", {
            "fields": (
                "created_at",
                "updated_at",
            ),
        }),
    )

    @admin.display(description="Thumbnail")
    def thumbnail_image(self, obj):

        if not obj.image.url:
            return "NO IMAGE"

        return format_html(
            '<img src="{}" style="width:45px; height:45px; '
            'object-fit:cover; border-radius:6px;" />',
            obj.image.url,
        )
    

# Blog Comment Admin
@admin.register(BlogComment)
class BlogCommentAdmin(ModelAdmin):

    list_display = (
        "id",
        "blog",
        "user",
        "content",
        "created_at",
        "updated_at",
    )

    list_display_links = (
        "id",
        "blog",
    )

    list_filter = (
        "created_at",
        "updated_at",
    )

    search_fields = (
        "blog__name",
        "user__username",
        "user__email",
        "content",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    list_per_page = 20

    fieldsets = (
        ("Comment Information", {
            "fields": (
                "blog",
                "user",
                "content",
            ),
        }),
        ("Timestamps", {
            "fields": (
                "created_at",
                "updated_at",
            ),
        }),
    )

# Blog Like Admin
@admin.register(BlogLike)
class BlogLikeAdmin(ModelAdmin):

    list_display = (
        "id",
        "blog",
        "user",
        "created_at",
    )

    list_display_links = (
        "id",
        "blog",
    )

    list_filter = (
        "created_at",
    )

    search_fields = (
        "blog__name",
        "user__username",
        "user__email",
    )

    readonly_fields = (
        "created_at",
    )

    list_per_page = 20

    fieldsets = (
        ("Like Information", {
            "fields": (
                "blog",
                "user",
            ),
        }),
        ("Timestamps", {
            "fields": (
                "created_at",
            ),
        }),
    )

# Blog Comment Like Admin
@admin.register(BlogCommentLike)
class BlogCommentLikeAdmin(ModelAdmin):

    list_display = (
        "id",
        "comment",
        "user",
        "created_at",
    )

    list_display_links = (
        "id",
        "comment",
    )

    list_filter = (
        "created_at",
    )

    search_fields = (
        "comment__content",
        "comment__blog__name",
        "user__username",
        "user__email",
    )

    readonly_fields = (
        "created_at",
    )

    list_per_page = 20

    fieldsets = (
        ("Comment Like Information", {
            "fields": (
                "comment",
                "user",
            ),
        }),
        ("Timestamps", {
            "fields": (
                "created_at",
            ),
        }),
    )