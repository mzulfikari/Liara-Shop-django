from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import View
from account.models import User, Otp
from .forms import LoginForm, CheckOtpform
from random import randint
from uuid import uuid4
from django.db import models
from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm
from django.urls import reverse
import ghasedakpack
from uuid import uuid4
from django.views.generic import TemplateView
from django.contrib import messages

# Api  رمز یکبار مصرف
# sms_api = ghasedakpack.Ghasedak(
#   '6a061b6d44718f16ccf3e790fcb4d8c45957118c275c1983986285c820a5ca34i9sbhbmD3sdJnmyN')

class UserLogin(View):

    @staticmethod
    def get(request):
        form = LoginForm()

        return render(
            request,
            "login.html",
            {
                "form": form,
                "next": request.GET.get("next", ""),
            }
        )

    def post(self, request):

        form = LoginForm(request.POST)

        if form.is_valid():

            valid = form.cleaned_data

            login_user = authenticate(
                username=valid["username"],
                password=valid["password"]
            )

            if login_user is not None:

                login(request, login_user)

                next_url = request.POST.get("next") or request.GET.get("next")

                if next_url:
                    return redirect(next_url)

                return redirect("Product:Product_view")

            else:

                form.add_error(
                    "username",
                    "اطلاعات وارد شده صحیح نمی باشد"
                )

        else:

            form.add_error(
                "username",
                "لطفا دوباره بررسی کنید اطلاعات وارد شده صحیح نمی باشد"
            )

        return render(
            request,
            "login.html",
            {
                "form": form,
                "next": request.POST.get("next", ""),
            }
        )

class UserRegister(View):
    """User login through phone number and email"""

    def get(self, request):
        form = RegisterForm()
        return render(request, "login-register.html", {"form": form})

    def post(self, request):
        phone = request.POST.get("phone")
        form = RegisterForm(request.POST)
        if form.is_valid():

            valid = form.cleaned_data
            randcode = randint(1000, 9999)
            # دریافت رمز یکبار مصرف
            # sms_api.verification({
            #     'receptor':valid["phone"],'type':'1','template':'randcode','param1':randcode
            # })
            token = str(uuid4())

            Otp.objects.create(phone=valid["phone"], code=randcode, token=token)

            return redirect(reverse("account:Verify") + f"?token={token}")
        else:
            form.add_error("phone", "اطلاعات وارد شده صحیح نمی باشد ")
        return render(request, "verify.html", {"form": form, "phone": phone})


class CheckOtp(View):
    """
    To authenticate the entered number and expire
    the one-time code within 2 minutes
    """

    def get(self, request):
        form = CheckOtpform()
        return render(request, "verify.html", {"form": form})

    def post(self, request):
        token = request.GET.get("token")
        form = CheckOtpform(request.POST)

        if form.is_valid():
            valid = form.cleaned_data

            if Otp.objects.filter(
                code=valid["code"],
                token=token,
            ).exists():
                otp = Otp.objects.get(token=token)

                if otp.is_expired:
                    form.add_error("code", "کد منقضی شده است")
                    return render(request, "verify.html", {"form": form})
                user, is_created = User.objects.get_or_create(
                    phone=otp.phone,
                )

                User.objects.create_user(
                    phone=form.cleaned_data.get("phone"),
                    last_name=form.cleaned_data.get("last_name"),
                    first_name=form.cleaned_data.get("first_name"),
                    password=form.cleaned_data.get("password"),
                )

                login(
                    request, user, backend="django.contrib.auth.backends.ModelBackend"
                )
                return redirect("/")

            otp.delete()

        else:
            form.add_error(None, "اطلاعات وارد شده صحیح نمی باشد ")

        return render(request, "verify.html", {"form": form})


def logout_user(request):
    logout(request)
    return redirect("/")
