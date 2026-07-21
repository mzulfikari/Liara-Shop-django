from django.db import models
from django.forms import ValidationError
from account.models import User
from account.managment.managment import UserManager
from django.contrib.auth import get_user_model


# پلتفرم مربوطه
class Platform(models.Model):
    title = models.CharField(
        max_length=50,
        verbose_name="رسانه های موجود",
        null=True,
        blank=True,
        choices=[
            ("اینستاگرام", "Instagram"),
            ("تلگرام", "Telegram"),
            ("واتساپ", "Whatsapp"),
            ("ایتا", "Eita"),
            ("روبیکا", "Rubika"),
        ],
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "مدیریت رسانه ها"


# تعریف Url & Utm
class Utm_info(models.Model):
    platform = models.ForeignKey(
        Platform, on_delete=models.SET_NULL, null=True, verbose_name="رسانه"
    )
    utm_source = models.CharField(max_length=200, verbose_name="منبع ورودی ")
    utm_medium = models.CharField(max_length=200, verbose_name="رسانه")
    utm_campaign = models.CharField(max_length=200, verbose_name="کمپین")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    base_url = models.URLField(verbose_name="لینک اصلی")

    sharing_url = models.URLField(
        blank=True, verbose_name="لینک اشتراک گذاری", primary_key=True, unique=True
    )

    def __str__(self):
        return f" {self.platform} | {self.utm_source} | {self.utm_medium} | {self.utm_campaign} "

    class Meta:
        verbose_name_plural = "مدیریت لینک ها"


# سطح دسترسی
class Utm_access(models.Model):
    ACCESS_LEVELS = [
        ("view", "مشاهده"),
        ("edit", "ویرایش"),
        ("delete", "pbt"),
    ]
    user_admin = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="انتخاب کاربر ادمین",
    )
    utm_info = models.ManyToManyField(Utm_info, verbose_name="لینک های قابل دسترس")
    access_level = models.CharField(
        max_length=30, verbose_name="سطح دسترسی کاریر ", choices=ACCESS_LEVELS
    )
    granted_at = models.DateTimeField(
        verbose_name="تاریخ اعطای دسترسی", auto_now_add=True
    )

    class Meta:
        verbose_name_plural = "سطح دسترسی به لینک ها "


# گزارشات
class Log_Utm(models.Model):
    platform = models.ForeignKey(
        Platform, on_delete=models.SET_NULL, null=True, verbose_name="عنوان رسانه"
    )
    url = models.ForeignKey(
        Utm_info, null=True, on_delete=models.SET_NULL, verbose_name="لینک رسانه"
    )
    views = models.SmallIntegerField(verbose_name="بازدید ها")
    cart = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "گزارشات "
