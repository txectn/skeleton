from django.contrib import admin
from unfold.admin import ModelAdmin

from ..models import SiteSetting

@admin.register(SiteSetting)
class SiteSettingAdmin(ModelAdmin):
    list_display = (
        "site_name",
        "email",
        "phone_number",
        "timezone",
        "default_currency",
        "updated_at",
    )

    search_fields = (
        "site_name",
        "email",
        "phone_number",
    )

    readonly_fields = (
        "updated_at",
    )