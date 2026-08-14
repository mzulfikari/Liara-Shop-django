from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
    )
from django.views.generic import View

from order.models import OrderModel, OrderStatusType
from .models import PaymentModel,PaymentStatusType
from django.urls import reverse_lazy
from .zarinpal_client import ZarinPalSandbox


class PaymentVerifyView(View):
    def get(self, request, *args, **kwargs):
        
        authority_id = request.GET.get("Authority")
        status = request.GET.get("Status")

        payment_obj = get_object_or_404(PaymentModel, authority_id=authority_id)
        order = OrderModel.objects.get(payment=payment_obj)

        zarin_pal = ZarinPalSandbox()
        response = zarin_pal.payment_verify(int(payment_obj.amount), payment_obj.authority_id)

        data = response.get("data")
        if data and data.get("code") in [100, 101]:
            payment_obj.ref_id = data.get("ref_id")
            payment_obj.response_code = data.get("code")
            payment_obj.status = PaymentStatusType.success.value
            payment_obj.response_json = response
            payment_obj.save()

            order.status = OrderStatusType.SUCCESS.value
            order.save()

            return redirect(reverse_lazy("order:completed"))
        else:
            error_code = response.get("errors", {}).get("code")
            payment_obj.response_code = error_code
            payment_obj.status = PaymentStatusType.failed.value
            payment_obj.response_json = response
            payment_obj.save()

            order.status = OrderStatusType.FAILED.value
            order.save()

            return redirect(reverse_lazy("order:failed"))