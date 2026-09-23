from django.contrib import admin

from ..models import SiteSetting

@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):

    list_display = (
        "site_name",
        "email",
        "phone_number",
        "timezone",
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