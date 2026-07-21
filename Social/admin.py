from django.contrib import admin
from . import models
from .models import Utm_info, Utm_access


@admin.register(models.Utm_info)
class Utm_info(admin.ModelAdmin):
    list_display = (
        "platform",
        "utm_source",
        "utm_medium",
        "utm_campaign",
        "created_at",
    )
    list_filter = (
        "utm_source",
        "platform",
    )
    readonly_fields = ["sharing_url", "created_at"]


@admin.register(models.Utm_access)
class Utm_Admin(admin.ModelAdmin):
    list_display = (
        "user_admin",
        "get_utm_info",
        "access_level",
        "granted_at",
    )

    def get_utm_info(self, obj):
        return str(obj.utm_info)

    get_utm_info.short_description = "utm_info"


@admin.register(models.Log_Utm)
class Utm_Logs(admin.ModelAdmin):
    list_display = (
        "platform",
        "url",
    )
    list_filter = ("platform", "url")


@admin.register(models.Platform)
class Platform_Admin(admin.ModelAdmin):
    list_display = ("title",)
