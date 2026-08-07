from django.contrib import admin
from .models import OrderModel, OrderItemModel, CouponModel


@admin.register(OrderModel)
class OrderModelAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "total_price",
        "coupon",
        "status",
        "created_date",
    ]

    list_display_links = ["id", "user"]

    search_fields = [
        "user__email",
        "user__phone",
        "id",
    ]

    list_filter = [
        "status",
        "created_date",
        "coupon",
    ]

    ordering = ["-created_date"]

    @admin.display(description="وضعیت سفارش")
    def status(self, obj):
        return obj.get_status()["label"]

    @admin.display(description="مبلغ کل")
    def total_price(self, obj):
        return f"{obj.total_price:,} تومان"

    @admin.display(description="کد سفارش")
    def id(self, obj):
        return obj.id


@admin.register(OrderItemModel)
class OrderItemModelAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "order",
        "product",
        "quantity",
        "price",
        "created_date",
    ]

    list_display_links = ["id", "product"]

    search_fields = [
        "product__title",
        "order__user__email",
        "order__id",
    ]

    list_filter = [
        "created_date",
    ]

    ordering = ["-created_date"]

    @admin.display(description="قیمت")
    def price(self, obj):
        return f"{obj.price:,} تومان"


@admin.register(CouponModel)
class CouponModelAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "code",
        "discount_percent",
        "max_limit_usage",
        "used_by_count",
        "expiration_date",
        "created_date",
    ]

    list_display_links = ["id", "code"]

    search_fields = [
        "code",
    ]

    list_filter = [
        "expiration_date",
        "created_date",
        "discount_percent",
    ]

    ordering = ["-created_date"]

    @admin.display(description="درصد تخفیف")
    def discount_percent(self, obj):
        return f"{obj.discount_percent}٪"

    @admin.display(description="تعداد مجاز استفاده")
    def max_limit_usage(self, obj):
        return f"{obj.max_limit_usage} بار"

    @admin.display(description="تعداد استفاده")
    def used_by_count(self, obj):
        return obj.used_by.all().count()
