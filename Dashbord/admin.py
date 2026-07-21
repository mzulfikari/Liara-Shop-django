from django.contrib import admin
from . import models
from jalali_date import datetime2jalali, date2jalali
from jalali_date.admin import ModelAdminJalaliMixin


@admin.register(models.Address)
class Address(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = [
        "user",
        "title",
        "first_name",
        "last_name",
        "city",
        "get_created_at_jalali",
    ]

    @admin.display(description="تاریخ ارسال", ordering="created_at")
    def get_created_at_jalali(self, obj):
        return datetime2jalali(obj.created_at).strftime("%a, %d %b  %Y _ %H:%M")


@admin.register(models.Notification)
class NotificationAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = [
        "short_message",
        "is_for_all_users",
        "is_active",
        "get_created_at_jalali",
        "get_expiration_date_jalali",
    ]
    list_filter = ["is_for_all_users", "is_active"]
    list_editable = ["is_active"]

    def short_message(self, obj):
        if len(obj.message) > 20:
            return obj.message[:20] + "..."
        return obj.message

    short_message.short_description = "پیام"

    @admin.display(description="تاریخ ایجاد", ordering="created_at")
    def get_created_at_jalali(self, obj):
        return datetime2jalali(obj.created_at).strftime("%a, %d %b %Y")

    @admin.display(description="تاریخ انقضا", ordering="expiration_date")
    def get_expiration_date_jalali(self, obj):
        if obj.expiration_date:
            return datetime2jalali(obj.expiration_date).strftime("%a, %d %b %Y")
        return "-"


@admin.register(models.Favorites)
class FavoritesAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ["user", "short_product_title", "get_created_at_jalali"]

    def short_product_title(self, obj):
        if len(obj.product.title) > 20:
            return obj.product.title[:20] + "..."
        return obj.product

    short_product_title.short_description = "محصول مربوطه"

    @admin.display(description="تاریخ ایجاد", ordering="created_at")
    def get_created_at_jalali(self, obj):
        return datetime2jalali(obj.created_at).strftime("%a, %d %b %Y")
