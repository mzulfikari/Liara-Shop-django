from decimal import Decimal
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from Products.models import Products
from Dashbord.models import Address


class OrderStatusType(models.IntegerChoices):
    PENDING = 1, "در انتظار پرداخت"
    SUCCESS = 2, "موفقیت‌آمیز"
    FAILED = 5, "لغو شده"


class CouponModel(models.Model):
    code = models.CharField(max_length=100, verbose_name="کد تخفیف")

    discount_percent = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="درصد تخفیف",
    )

    max_limit_usage = models.PositiveIntegerField(
        default=10, verbose_name="حداکثر تعداد استفاده"
    )

    used_by = models.ManyToManyField(
        "account.User",
        related_name="coupon_users",
        blank=True,
        verbose_name="استفاده‌کنندگان",
    )

    expiration_date = models.DateTimeField(
        null=True, blank=True, verbose_name="تاریخ انقضا"
    )

    created_date = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    updated_date = models.DateTimeField(
        auto_now=True, verbose_name="تاریخ آخرین بروزرسانی"
    )

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = "کد تخفیف"
        verbose_name_plural = "کدهای تخفیف"
        ordering = ["-created_date"]


class OrderModel(models.Model):

    user = models.ForeignKey(
        "account.User", on_delete=models.PROTECT, verbose_name="کاربر"
    )

    address = models.ForeignKey(
        Address,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="آدرس ارسال",
    )

    payment = models.ForeignKey(
        "pyment.PaymentModel",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="پرداخت",
    )

    total_price = models.DecimalField(
        default=0,
        max_digits=10,
        decimal_places=0,
        null=True,
        blank=True,
        verbose_name="مبلغ کل",
    )

    coupon = models.ForeignKey(
        CouponModel,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="کد تخفیف",
    )

    status = models.IntegerField(
        choices=OrderStatusType.choices,
        default=OrderStatusType.PENDING.value,
        verbose_name="وضعیت سفارش",
    )

    created_date = models.DateTimeField(
        auto_now_add=True, verbose_name="تاریخ ثبت سفارش"
    )

    updated_date = models.DateTimeField(
        auto_now=True, verbose_name="تاریخ آخرین بروزرسانی"
    )

    class Meta:
        verbose_name = "سفارش"
        verbose_name_plural = "سفارش‌ها"
        ordering = ["-created_date"]

    def calculate_total_price(self):
        return sum(item.price * item.quantity for item in self.order_items.all())

    def get_status(self):
        return {
            "id": self.status,
            "title": OrderStatusType(self.status).name,
            "label": OrderStatusType(self.status).label,
        }

    def get_full_address(self):
        if self.address:
            return (
                f"{self.address.province}، "
                f"{self.address.city}، "
                f"{self.address.full_address}"
            )

        return "آدرس ثبت نشده است"

    def __str__(self):
        return f"{self.user.email} - سفارش {self.id}"

    @property
    def is_successful(self):
        return self.status == OrderStatusType.SUCCESS.value

    def get_price(self):

        if self.coupon:
            discount = (
                self.total_price
                * Decimal(self.coupon.discount_percent)
                / Decimal("100")
            )

            return round(self.total_price - discount)

        return self.total_price


class OrderItemModel(models.Model):

    order = models.ForeignKey(
        OrderModel,
        on_delete=models.CASCADE,
        related_name="order_items",
        verbose_name="سفارش",
    )

    product = models.ForeignKey(
        Products, on_delete=models.CASCADE, verbose_name="محصول"
    )

    quantity = models.PositiveIntegerField(default=0, verbose_name="تعداد")

    price = models.DecimalField(
        default=0, max_digits=10, decimal_places=0, verbose_name="قیمت"
    )

    created_date = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    updated_date = models.DateTimeField(
        auto_now=True, verbose_name="تاریخ آخرین بروزرسانی"
    )

    def __str__(self):
        return f"{self.product.title} - {self.id}"

    class Meta:
        verbose_name = "آیتم سفارش"
        verbose_name_plural = "آیتم‌های سفارش"
        ordering = ["-created_date"]
