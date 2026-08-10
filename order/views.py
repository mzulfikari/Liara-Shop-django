from django.shortcuts import render, redirect
from django.views.generic import FormView, TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from decimal import Decimal
from django.http import JsonResponse
from django.utils import timezone
from order.models import OrderModel
from order.models import OrderModel, OrderItemModel, CouponModel
from .forms import CheckOutForm
from django.urls import reverse_lazy
from Cart.cart import CartSession
from Cart.models import CartModel
from pyment.zarinpal_client import ZarinPalSandbox
from pyment.models import PaymentModel
from Dashbord.models import Address

class OrderView(TemplateView):
    
    template_name = 'checkout.html'

class OrderCheckOutView(LoginRequiredMixin, FormView):
    template_name = "checkout.html"
    form_class = CheckOutForm
    success_url = reverse_lazy("order:completed")

    def get_form_kwargs(self):
        kwargs = super(OrderCheckOutView, self).get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_valid(self, form):
        user = self.request.user
        cleaned_data = form.cleaned_data
        address = cleaned_data["address_id"]
        coupon = cleaned_data["coupon"]

        cart = CartModel.objects.get(user=user)
        order = self.create_order(address)

        self.create_order_items(order, cart)
        self.clear_cart(cart)

        total_price = order.calculate_total_price()
        order.total_price = total_price
        self.apply_coupon(coupon, order, user, total_price)
        order.save()
        return redirect(self.create_payment_url(order))

    def create_payment_url(self, order):
        zarinpal = ZarinPalSandbox()
        amount_in_rial = order.total_price * 10

        if amount_in_rial < 1000:
            raise ValueError("مبلغ سفارش کمتر از حداقل مجاز زرین‌پال است")

        response = zarinpal.payment_request(amount_in_rial)

        data = response.get("data")
        if not data or data.get("code") != 100:
            raise ValueError(f"ZarinPal request failed: {response}")

        authority = data.get("authority")
        payment_obj = PaymentModel.objects.create(
            authority_id=authority,
            amount=amount_in_rial,
        )
        order.payment = payment_obj
        order.save()
        return zarinpal.generate_payment_url(authority)

    def create_order(self, address):
        return OrderModel.objects.create(
            user=self.request.user,
            address=address.address,
            state=address.state,
            city=address.city,
            zip_code=address.zip_code,
        )

    def create_order_items(self, order, cart):
        for item in cart.cart_items.all():
            OrderItemModel.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.get_price(),
            )

    def clear_cart(self, cart):
        cart.cart_items.all().delete()
        CartSession(self.request.session).clear()

    def apply_coupon(self, coupon, order, user, total_price):
        if coupon:
            # discount_amount = round(
            #     (total_price * Decimal(coupon.discount_percent / 100)))
            # total_price -= discount_amount

            order.coupon = coupon
            coupon.used_by.add(user)
            coupon.save()
        order.total_price = total_price

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = CartModel.objects.get(user=self.request.user)
        context["addresses"] = Address.objects.filter(user=self.request.user)
        total_price = cart.calculate_total_price()
        context["total_price"] = total_price
        context["total_tax"] = round((total_price * 9) / 100)
        return context


class OrderCompletedOutView(TemplateView):

    template_name = "order/order-completed.html"


class OrderFailedView(TemplateView):

    template_name = "order/order-failed.html"


class ValidateCouponView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        code = request.POST.get("code")
        user = self.request.user

        status_code = 200
        message = "کد تخفیف با موفقیت ثبت شد"
        total_price = 0
        total_tax = 0

        try:
            coupon = CouponModel.objects.get(code=code)
        except CouponModel.DoesNotExist:
            return JsonResponse({"message": "کد تخفیف یافت نشد"}, status=404)
        else:
            if coupon.used_by.count() >= coupon.max_limit_usage:
                status_code, message = 403, "محدودیت در تعداد استفاده"

            elif coupon.expiration_date and coupon.expiration_date < timezone.now():
                status_code, message = 403, "کد تخفیف منقضی شده است"

            elif user in coupon.used_by.all():
                status_code, message = 403, "این کد تخفیف قبلا توسط شما استفاده شده است"
            else:
                cart = CartModel.objects.get(user=self.request.user)

                total_price = cart.calculate_total_price()
                total_price = round(
                    total_price - (total_price * coupon.discount_percent / 100)
                )
                total_tax = round(total_price * 9 / 100)
        return JsonResponse(
            {"message": message, "total_tax": total_tax, "total_price": total_price},
            status=status_code,
        )
