from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.html import format_html


STATUS = (
    ("draft", "پیش نویس شود"),
    ("published", "منتشر شود"),
)

Performance_Venue = (
    ("Header", "بنر هدر سایت"),
    ("Banner for Heavily Discounted Products", "بنر محصولات پرتخفیف "),
    ("Banner 1.1", "1.1 بنر"),
    ("Banner 1.2", "1.2 بنر"),
    ("Banner 1.3", "1.3 بنر"),
    ("Banner 1.4", "1.4 بنر"),
    ("Banner 2.1", "2.1 بنر"),
    ("Banner 2.2", "2.2 بنر"),
)

class SiteSettings(models.Model):
    
    title = models.CharField(
        max_length=100,null=True,blank=True,verbose_name='عنوان فروشگاه'
    )
    logo = models.ImageField( 
        upload_to='logo/image',null=True,blank=True,verbose_name='لوگو'
        )
    text_about_us = CKEditor5Field(
        null=True, blank=True, verbose_name='متن درباره ما بخش فوتر',config_name='default'
        )
    address = models.CharField(
        max_length=350, null=True, blank=True, verbose_name='آدرس'
        )
    phone1 = models.CharField(
        max_length=14, null=True, blank=True, verbose_name='شماره تلفن همراه'
        )
    phone2 = models.CharField(
        max_length=14, null=True, blank=True, verbose_name='شماره تلفن ثابت'
        )
    email1 = models.CharField(
        max_length=250, null=True, blank=True, verbose_name='ایمیل '
        )
    instagram_link = models.CharField(
        max_length=250, null=True, blank=True, default='https://instagram.com/username', verbose_name='لینک اینستاگرام'
        )
    telegram_link = models.CharField(
        max_length=250, null=True, blank=True, default='https://t.me/username', verbose_name='لینک تلگرام'
        )
    
    def __str__(self):
        return self.title
    
    def show_image(self):
        """To display images in the management panel"""

        if self.logo:
            return format_html(f'<img src="{self.logo.url}" width="78 px" height="50" />')
        return format_html('<h3 style="color: red">تصویر ندارد</h3>')
    show_image.short_description = " تصویر"


    class Meta:
        verbose_name = 'تنظیمات سایت'
        verbose_name_plural = 'تنظیمات سایت'


class Banner(models.Model):
    title = models.CharField(
        max_length=200, verbose_name='عنوان بنر'
        )
    image = models.ImageField(
        upload_to='banners/', verbose_name='تصویر بنر'
        )
    status = models.CharField(
        choices=STATUS, max_length=10, default='published', verbose_name='وضعیت'
        )
    pformance_Venue =  models.CharField(
        choices=Performance_Venue, max_length=50, default='Header', verbose_name='جایگاه نمایش'
        )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='تاریخ ایجاد'
        )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='تاریخ به‌روزرسانی'
        )
    
    
    def show_image(self):
        """To display images in the management panel"""

        if self.image:
            return format_html(f'<img src="{self.image.url}" width="78 px" height="50" />')
        return format_html('<h3 style="color: red">تصویر ندارد</h3>')
    show_image.short_description = " تصویر"

        
    
    class Meta:
        verbose_name = 'بنر'
        verbose_name_plural = 'بنر ها'


    def banner_image(self):
        if self.image:
            return format_html(f'<img src="{self.image.url}" width="100px" height="50px">')
        return format_html(f'<h3 style="color: red">تصویر ندارد</h3>')

    def __str__(self):
        return self.title
    
    
    
class ContactUs(models.Model):
    first_name = models.CharField(
        max_length=100, verbose_name='نام'
        )
    last_name = models.CharField(
        max_length=100, verbose_name='نام خانوادگی'
        )
    phone = models.CharField(
        max_length=14, verbose_name='شماره تماس'
        )
    message = models.TextField(
        verbose_name='متن پیام'
        )
    date_send = models.DateTimeField(
        auto_now_add=True, verbose_name='تاریخ ارسال'
        )

    class Meta:
        ordering = ["-date_send"]
        verbose_name = "تماس با ما"
        verbose_name_plural = "تماس با ما"

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    

class About_Me(models.Model):
    title =  models.CharField(
        max_length=60, blank=True, null=True,verbose_name='عنوان'
        )
    image = models.ImageField(
        blank=True,null=True,verbose_name='تصویر'
        )
    text = CKEditor5Field(
        null=True, blank=True, verbose_name='متن درباره ما',config_name='default'
        )
    def __str__(self):
        return self.title
    
    def image_about_me(self):
        if self.image:
            return format_html(f'<img src="{self.image.url}" width="100px" height="50px">')
        return format_html(f'<h3 style="color: red">تصویر ندارد</h3>')
    class Meta:
        verbose_name = "درباره ما"
        verbose_name_plural = "درباره ما"
