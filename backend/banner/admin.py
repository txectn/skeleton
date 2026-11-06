from django import forms
from django.contrib import admin

from django.utils.html import format_html

from unfold.admin import ModelAdmin

from .models import Banner

class BannerAdminForm(forms.ModelForm):

    class Meta:
        model = Banner
        fields = "__all__"

    def clean(self):

        cleaned_data = super().clean()

        destination_type = cleaned_data.get("destination_type")

        required_fields = {
            Banner.DestinationType.COLLECTION: "collection",
            Banner.DestinationType.PROMOTION: "promotion",
            Banner.DestinationType.PRODUCT: "product",
            Banner.DestinationType.CUSTOM_URL: "custom_url",
        }

        field_name = required_fields.get(destination_type)

        if field_name and not cleaned_data.get(field_name):
            self.add_error(
                field_name,
                "Please select a destination before saving.",
            )

        return cleaned_data

@admin.register(Banner)
class BannerAdmin(ModelAdmin):

    form = BannerAdminForm

    list_display = (
        "thumbnail_image",
        "id",
        "title",
        "destination_type",
        "position",
        "is_active",
        "starts_at",
        "ends_at",
        "created_at",
    )

    list_display_links = (
        "thumbnail_image",
        "id",
        "title",
    )

    list_filter = (
        "is_active",
        "destination_type",
        "created_at",
    )

    search_fields = (
        "title",
        "heading",
        "subtitle",
    )

    ordering = (
        "position",
        "-created_at",
    )

    list_editable = (
        "position",
        "is_active",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    date_hierarchy = "created_at"

    fieldsets = (

        ("Banner Information", {
            "fields": (
                "title",
                "heading",
                "subtitle",
                "image",
                "mobile_image",
            ),
        }),

        ("Destination", {
            "fields": (
                "destination_type",
                "collection",
                "promotion",
                "product",
                "custom_url",
            ),
        }),

        ("Call To Action", {
            "fields": (
                "cta_label",
            ),
        }),

        ("Display Settings", {
            "fields": (
                "position",
                "is_active",
                "starts_at",
                "ends_at",
            ),
        }),

        ("Timestamps", {
            "classes": ("collapse",),
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