from django.contrib import admin
from unfold.admin import ModelAdmin, StackedInline

from .models import (
    AboutPage,
    AboutSection,
    AboutItem,
)

# =====================================
# About Item Inline
# =====================================

class AboutItemInline(StackedInline):

    model = AboutItem

    extra = 0
    min_num = 0

    fields = (
        "title",
        "description",
        "icon",
    )

# =====================================
# About Section Inline
# =====================================

class AboutSectionInline(StackedInline):

    model = AboutSection

    extra = 0
    min_num = 1

    fields = (
        "section_id",
        "title",
        "heading",
        "description",
        "cta_label",
        "cta_link",
        "position",
        "image_position",
        "image",
    )

    ordering = (
        "position",
    )

    inlines = (
        AboutItemInline,
    )

# =====================================
# About Page Admin
# =====================================

@admin.register(AboutPage)
class AboutPageAdmin(ModelAdmin):

    list_display = (
        "id",
        "is_active",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "is_active",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fields = (
        "is_active",
        "created_at",
        "updated_at",
    )

    ordering = (
        "-created_at",
    )

    inlines = (
        AboutSectionInline,
    )