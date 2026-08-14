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
    """Register user with phone number and send OTP."""

    template_name = "login-register.html"

    def get(self, request):
        form = RegisterForm()

        return render(
            request,
            self.template_name,
            {"form": form},
        )

    def post(self, request):
        form = RegisterForm(request.POST)

        if not form.is_valid():
            return render(
                request,
                self.template_name,
                {"form": form},
            )

        phone = form.cleaned_data["phone"]

        # بررسی وجود کاربر
        if User.objects.filter(phone=phone).exists():
            form.add_error(
                "phone",
                "این شماره همراه قبلاً ثبت‌نام کرده است.",
            )

            return render(
                request,
                self.template_name,
                {"form": form},
            )

        # ساخت کاربر
        user = User.objects.create_user(
            phone=phone,
            first_name=form.cleaned_data["first_name"],
            last_name=form.cleaned_data["last_name"],
            password=form.cleaned_data["password"],
        )

        # ساخت OTP
        code = randint(1000, 9999)
        token = str(uuid4())

        Otp.objects.create(
            phone=phone,
            code=code,
            token=token,
        )

        # TODO: ارسال SMS
        #
        # sms_api.verification({
        #     "receptor": phone,
        #     "type": "1",
        #     "template": "randcode",
        #     "param1": code,
        # })

        verify_url = reverse("account:Verify")

        return redirect(
            f"{verify_url}?token={token}"
        )


class CheckOtp(View):
    """Verify OTP and login user."""

    template_name = "verify.html"

    def get(self, request):
        token = request.GET.get("token")

        form = CheckOtpform()

        return render(
            request,
            self.template_name,
            {
                "form": form,
                "token": token,
            },
        )

    def post(self, request):
        token = request.GET.get("token")

        form = CheckOtpform(request.POST)

        if not token:
            form.add_error(
                None,
                "توکن احراز هویت نامعتبر است.",
            )

            return render(
                request,
                self.template_name,
                {"form": form},
            )

        if not form.is_valid():
            return render(
                request,
                self.template_name,
                {
                    "form": form,
                    "token": token,
                },
            )

        code = int(form.cleaned_data["code"])

        # پیدا کردن OTP
        otp = Otp.objects.filter(
            token=token,
            phone__isnull=False,
        ).first()

        if not otp:
            form.add_error(
                "code",
                "کد تأیید معتبر نیست.",
            )

            return render(
                request,
                self.template_name,
                {
                    "form": form,
                    "token": token,
                },
            )

        # بررسی اعتبار OTP
        if not otp.is_valid(code):
            form.add_error(
                "code",
                "کد تأیید اشتباه یا منقضی شده است.",
            )

            return render(
                request,
                self.template_name,
                {
                    "form": form,
                    "token": token,
                },
            )

        # پیدا کردن کاربر
        user = User.objects.filter(
            phone=otp.phone
        ).first()

        if not user:
            form.add_error(
                None,
                "کاربر مربوط به این کد پیدا نشد.",
            )

            return render(
                request,
                self.template_name,
                {
                    "form": form,
                    "token": token,
                },
            )

        # OTP با موفقیت استفاده شد
        otp.is_used = True
        otp.save(update_fields=["is_used"])

        # ورود کاربر
        login(
            request,
            user,
            backend="django.contrib.auth.backends.ModelBackend",
        )

        return redirect("/")
    
    
def logout_user(request):
    logout(request)
    return redirect("/")
