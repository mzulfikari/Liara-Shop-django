from django.db import models
from account.models import User


class CartModel(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر")

    created_date = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    updated_date = models.DateTimeField(
        auto_now=True, verbose_name="تاریخ آخرین بروزرسانی"
    )

    def __str__(self):
        return self.user.phone

    def calculate_total_price(self):
        return sum(
            item.product.get_price() * item.quantity for item in self.cart_items.all()
        )

    class Meta:
        verbose_name = "سبد خرید"
        verbose_name_plural = "سبدهای خرید"
        ordering = ["-created_date"]


class CartItemModel(models.Model):

    cart = models.ForeignKey(
        CartModel,
        on_delete=models.CASCADE,
        related_name="cart_items",
        verbose_name="سبد خرید",
    )

    product = models.ForeignKey(
        "Products.Products", on_delete=models.PROTECT, verbose_name="محصول"
    )

    quantity = models.PositiveIntegerField(default=0, verbose_name="تعداد")

    created_date = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    updated_date = models.DateTimeField(
        auto_now=True, verbose_name="تاریخ آخرین بروزرسانی"
    )

    def __str__(self):
        return f"{self.product.title} - {self.cart.id}"

    class Meta:
        verbose_name = "آیتم سبد خرید"
        verbose_name_plural = "آیتم‌های سبد خرید"
        ordering = ["-created_date"]
