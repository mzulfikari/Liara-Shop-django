from datetime import timedelta
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from account.managment.managment import UserManager
from django.utils.translation import gettext as _
from utils.validator import *
from django.core.validators import RegexValidator
from Products.models import *

def otp_expiry():
    return timezone.now() + timedelta(minutes=2)

class User(AbstractBaseUser):
    """User profile that authenticates and
    logs in with a phone number or email"""

    phone = models.CharField(
        verbose_name="شماره تلفن",
        max_length=255,
        unique=True,
        validators=[
            RegexValidator(
                regex=r"^09\d{9}$",
                message="شماره تلفن باید با 09 شروع شده و 11 رقم باشد",
            )
        ],
    )
    first_name = models.CharField(max_length=50, verbose_name="نام")
    last_name = models.CharField(max_length=50, verbose_name="نام خانوادگی")
    verification_time = models.DateField(verbose_name="تاریخ عضویت ", auto_now_add=True)
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    is_admin = models.BooleanField(verbose_name="وضعیت ادمین", default=False)
    email = models.EmailField(verbose_name="ایمیل", null=True, blank=True)
    image = models.ImageField(
        upload_to="profile/imag", null=True, blank=True, verbose_name="پروفایل"
    )
    password = models.CharField(max_length=300)
    national_code = models.CharField(
        validators=[
            persian_national_code,
        ],
        null=True,
        blank=True,
        verbose_name="کد ملی",
        max_length=10,
    )
    card_number = models.CharField(
        max_length=16,
        validators=[
            RegexValidator(
                regex=r"^\d{16}$",
                message="شماره کارت باید 16 رقم باشد",
                code="invalid_card_number",
            )
        ],
        null=True,
        blank=True,
        verbose_name="شماره کارت",
    )

    objects = UserManager()

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):

        return self.is_admin

    class Meta:
        verbose_name = "پروفایل"
        verbose_name_plural = "پروفایل ها"


# ریجستر و احراز هویت شماره تلفن
class Otp(models.Model):
    """Authentication related model
    with token creation feature
    """

    token = models.CharField(max_length=200, null=True, verbose_name="توکن")
    phone = models.CharField(
        max_length=11,
        validators=[
            RegexValidator(
                regex=r"^09\d{9}$",
                message="شماره تلفن باید با 09 شروع شده و 11 رقم باشد",
            )
        ],
        verbose_name="شماره تلفن",
    )

    code = models.SmallIntegerField(verbose_name="کد یکبار مصرف")
    code_expiry = models.DateTimeField(
    verbose_name="تاریخ انقضای کد",
    default=otp_expiry,
    )
    is_used = models.BooleanField(default=False, verbose_name="استفاده شده؟")

    class Meta:
        verbose_name = "رمز یکبار مصرف"
        verbose_name_plural = " احراز هویت Otp"

    def is_valid(self, code):
        if self.code == code and not self.is_used and self.code_expiry:
            if timezone.now() <= self.code_expiry:
                return True
            else:
                self.delete()
                return False
        return False

    def set_code(self, code):
        self.code = code
        self.code_expiry = timezone.now() + timedelta(minutes=2)
        self.save()

    @classmethod
    def clean_expired_codes(cls):
        cls.objects.filter(
            models.Q(is_used=True) | models.Q(code_expiry__lt=timezone.now())
        ).delete()


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        User.objects.create(user=instance)


def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
