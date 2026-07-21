from django.db import models
from django.urls import reverse
from django.utils.html import format_html
from account.models import User
from django.utils.text import slugify
from django.utils.translation import gettext as _
from colorfield.fields import ColorField
from django.utils.text import slugify


class ProductStatusType(models.IntegerChoices):
    publish = 1, ("نمایش")
    draft = 2, ("عدم نمایش")


class Category(models.Model):
    title = models.CharField(max_length=50, verbose_name="عنوان")
    image = models.ImageField(
        verbose_name="تصویر دسته بندی",
        upload_to="category/image",
        null=True,
        blank=True,
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    views = models.BooleanField(default=True, verbose_name="نمایش در صحفه اصلی ")
    slug = models.SlugField(
        verbose_name="نامک",
        help_text="مقدار به صورت خودکار از عنوان محصول استلفاده می شود",
        blank=True,
        unique=True,
    )

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.slug = slugify(self.title, allow_unicode=True)
        super(Category, self).save()

    def __str__(self):
        return self.title

    def show_image(self):
        """To display images in the management panel"""
        if self.image:
            return format_html(
                f'<img src="{self.image.url}" width="78 px" height="50" />'
            )
        return format_html('<h3 style="color: red">تصویر ندارد</h3>')

    show_image.short_description = " تصاویر"

    class Meta:
        verbose_name_plural = "دسته بندی ها"


class Size(models.Model):
    title = models.CharField(max_length=30)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "سایز"


class Color(models.Model):
    title = models.CharField(
        max_length=30,
        verbose_name="عنوان رنگ",
        help_text="لطفا عنوان را خالی نگذارید",
    )
    color_code = ColorField(
        max_length=20,
        unique=True,
        default="#229605",
        help_text="این یک کد رنگی است",
        verbose_name="کد رنگ",
    )
    created = models.DateTimeField(
        auto_now_add=True, verbose_name="تاریخ ایجاد", null=True
    )

    def __str__(self):
        return f"{self.title} ({self.color_code})"

    class Meta:
        verbose_name_plural = "رنگ بندی "


class Brand(models.Model):
    title = models.CharField(max_length=60, verbose_name="برند", blank=True, null=True)
    image = models.ImageField(
        upload_to="product/image/brand",
        blank=True,
        null=True,
        verbose_name=" بارگذاری تصویر"
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "برند ها "


class Products(models.Model):
    title = models.CharField(max_length=80, verbose_name="عنوان")
    hover_title = models.CharField(
        max_length=60, verbose_name="عنوان معرفی", blank=True, null=True
    )
    image = models.ImageField(
        upload_to="product/image",
        blank=True,
        null=True,
        verbose_name=" بارگذاری تصویر اصلی",
    )
    image_subset_1 = models.ImageField(
        upload_to="product/image",
        blank=True,
        null=True,
        verbose_name=" بارگذاری تصویر دوم",
    )
    image_subset_2 = models.ImageField(
        upload_to="product/image",
        blank=True,
        null=True,
        verbose_name="بارگذاری تصویر سوم ",
    )
    image_subset_3 = models.ImageField(
        upload_to="product/image",
        blank=True,
        null=True,
        verbose_name=" بارگذاری تصویر چهارم",
    )
    price = models.DecimalField(
        verbose_name="قیمت",
        max_digits=10,
        decimal_places=0,
    )
    caption = models.TextField(verbose_name="درباره محصول")
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="دسته بندی",
        related_name="products",
    )
    size = models.ManyToManyField(
        Size, blank=True, related_name="products", verbose_name="سایزها"
    )
    color = models.ManyToManyField(
        Color, related_name="products", verbose_name="رنگ بندی ها", blank=True
    )
    status = models.IntegerField(
        choices=ProductStatusType.choices,
        default=ProductStatusType.draft.value,
        verbose_name="وضعیت نمایش",
    )
    stock_count = models.IntegerField(
        verbose_name=" تعداد موجودی", null=True, blank=True
    )
    created = models.DateTimeField(
        auto_now_add=True, verbose_name="تاریخ ایجاد", null=True
    )
    views = models.IntegerField(default=0, editable=False, verbose_name="بازدید")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ به‌روزرسانی")
    # brand = models.ForeignKey(
    #     Brand,verbose_name='برند'
    # )
    slug = models.SlugField(
        verbose_name="نامک",
        help_text="مقدار به صورت خودکار از عنوان محصول استلفاده می شود",
        blank=True,
        unique=True,
    )
    Discounts = models.BooleanField(
        verbose_name=" نمایش در پرتخفیف ترین ها",
        default=False,
    )

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.slug = slugify(self.title, allow_unicode=True)
        super(Products, self).save()

    def __str__(self):
        return self.title

    def show_image(self):
        """To display images in the management panel"""

        if self.image:
            return format_html(
                f'<img src="{self.image.url}" width="78 px" height="50" />'
            )
        return format_html('<h3 style="color: red">تصویر ندارد</h3>')

    show_image.short_description = " تصاویر"

    class Meta:
        ordering = ["-created"]
        verbose_name_plural = "محصولات"


class Information(models.Model):
    product = models.ForeignKey(
        Products,
        on_delete=models.CASCADE,
        related_name="information",
        verbose_name="محصول",
    )
    Feature_title = models.CharField(
        max_length=80, blank=True, null=True, verbose_name="عنوان ویژگی"
    )
    Featur = models.CharField(
        max_length=60, blank=True, null=True, verbose_name="ویژگی"
    )

    def __str__(self):
        return f"{self.product.title} - {self.Feature_title or ''}: {self.Featur or ''}"

    class Meta:
        verbose_name_plural = "ویژگی ها"


class Comment(models.Model):
    """Implementation of the questions section,
    which features questions and answers after login"""

    STATUS = (
        ("Awaiting confirmation", "در انتظار تایید"),
        ("It was confirmed", "تایید شد"),
        ("rejected", "رد شد"),
    )
    products = models.ForeignKey(
        Products,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="محصول",
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments", verbose_name="کاربر"
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="replies",
        null=True,
        blank=True,
        verbose_name="پاسخ ها ",
    )
    body = models.TextField(verbose_name="نظر")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    status = models.CharField(
        choices=STATUS,
        max_length=30,
        default="Awaiting confirmation",
        verbose_name="وضعیت",
    )

    def __str__(self):
        return self.products.title

    class Meta:
        verbose_name_plural = "نظرات"
