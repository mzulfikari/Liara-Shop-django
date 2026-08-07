from django.db import models
from django.db.models import JSONField


class PaymentStatusType(models.IntegerChoices):
    pending = 1, "در انتظار پرداخت"
    success = 2, "پرداخت موفق"
    failed = 3, "پرداخت ناموفق"


class PaymentModel(models.Model):

    authority_id = models.CharField(max_length=255, verbose_name="شناسه اعتبار پرداخت")

    ref_id = models.BigIntegerField(
        null=True, blank=True, verbose_name="شناسه مرجع پرداخت"
    )

    amount = models.DecimalField(
        default=0, max_digits=10, decimal_places=0, verbose_name="مبلغ پرداخت"
    )

    response_json = JSONField(default=dict, verbose_name="اطلاعات پاسخ درگاه")

    response_code = models.IntegerField(
        null=True, blank=True, verbose_name="کد پاسخ درگاه"
    )

    status = models.IntegerField(
        choices=PaymentStatusType.choices,
        default=PaymentStatusType.pending.value,
        verbose_name="وضعیت پرداخت",
    )

    created_date = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    updated_date = models.DateTimeField(
        auto_now=True, verbose_name="تاریخ آخرین بروزرسانی"
    )

    class Meta:
        verbose_name = "پرداخت"
        verbose_name_plural = "پرداخت‌ها"
        ordering = ["-created_date"]

    def __str__(self):
        return f"{self.authority_id} - {self.amount}"
