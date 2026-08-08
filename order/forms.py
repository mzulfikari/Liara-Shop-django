from django import forms
from order.models import CouponModel
from django.utils import timezone
from Dashbord.models import Address

class CheckOutForm(forms.Form):

    address_id = forms.IntegerField(
        required=True,
        error_messages={
            "required": "لطفاً یک آدرس را انتخاب کنید",
            "invalid": "آدرس معتبر نیست",
        },
    )

    coupon = forms.CharField(
        required=False,
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(CheckOutForm, self).__init__(*args, **kwargs)

    def clean_address_id(self):
        address_id = self.cleaned_data.get("address_id")
        user = self.request.user

        try:
            address = Address.objects.get(
                id=address_id,
                user=user,
            )

        except Address.DoesNotExist:
            raise forms.ValidationError(
                "لطفاً یک آدرس را انتخاب کنید"
            )

        return address

    def clean_coupon(self):
        code = self.cleaned_data.get("coupon")
        if code == "":
            return None
        # Check if the address_id belongs to the requested user
        user = self.request.user  # Assuming the user is available in the request object
        coupon = None
        try:
            coupon = CouponModel.objects.get(code=code)
        except CouponModel.DoesNotExist:
            raise forms.ValidationError("کد تخفیف اشتباه است")
        if coupon:

            if coupon.used_by.count() >= coupon.max_limit_usage:
                raise forms.ValidationError("محدودیت در تعداد استفاده")

            if coupon.expiration_date and coupon.expiration_date < timezone.now():
                raise forms.ValidationError("کد تخفیف منقضی شده است")

            if user in coupon.used_by.all():
                raise forms.ValidationError(
                    "این کد تخفیف قبلا توسط شما استفاده شده است"
                )

        return coupon
