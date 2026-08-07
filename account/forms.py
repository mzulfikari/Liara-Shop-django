import re
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from account.models import User, Otp


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ["phone", "last_name"]

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("گذرواژه ها مطابقت ندارند")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = [
            "phone",
            "password",
            "first_name",
            "last_name",
            "is_active",
            "is_admin",
        ]


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "w-full drop-shadow-lg outline-none rounded-2xl py-2 text-center",
                "placeholder": "شماره همراه یا ایمیل ",
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full drop-shadow-lg outline-none rounded-2xl py-2 text-center",
                "placeholder": "رمز عبور",
            }
        )
    )

    def clean_username(self):
        username = self.cleaned_data.get("username")

        if not username:
            raise ValidationError("لطفاً ایمیل یا شماره همراه را وارد کنید.")

        phone_pattern = r"^09\d{9}$"
        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

        if re.match(phone_pattern, username):
            return username

        if re.match(email_pattern, username):
            return username

        raise ValidationError(
            "فرمت وارد شده صحیح نیست. لطفاً ایمیل یا شماره همراه معتبر وارد کنید."
        )

    def clean_password(self):
        password = self.cleaned_data.get("password")

        if not password:
            raise ValidationError("رمز عبور الزامی است.")

        if len(password) < 8:
            raise ValidationError("رمز عبور باید حداقل ۸ کاراکتر باشد.")

        return password


class RegisterForm(forms.Form):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "w-full drop-shadow-lg outline-none rounded-2xl py-2 text-center"
            }
        )
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "w-full drop-shadow-lg outline-none rounded-2xl py-2 text-center"
            }
        ),
    )
    phone = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "w-full drop-shadow-lg outline-none rounded-2xl py-2 text-center"
            }
        ),
        min_length=11,
        max_length=11,
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full drop-shadow-lg outline-none rounded-2xl py-2 text-center"
            }
        ),
        min_length=8,
        max_length=20,
    )

    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")

        if not first_name:
            raise ValidationError("لطفاً نام را وارد کنید.")

        if not re.match(r"^[آ-یa-zA-Z\s]+$", first_name):
            raise ValidationError("نام فقط می‌تواند شامل حروف باشد.")

        if len(first_name.strip().split()) < 1:
            raise ValidationError("نام معتبر نیست.")

        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name")

        if not last_name:
            raise ValidationError("لطفاً نام خانوادگی را وارد کنید.")

        if not re.match(r"^[آ-یa-zA-Z\s]+$", last_name):
            raise ValidationError("نام خانوادگی فقط می‌تواند شامل حروف باشد.")

        if len(last_name) < 3:
            raise ValidationError("نام خانوادگی باید حداقل 3 حرف باشد.")

        return last_name

    def clean_password(self):
        password = self.cleaned_data.get("password")

        if not password:
            raise ValidationError("رمز عبور الزامی است.")

        if len(password) < 8:
            raise ValidationError("رمز عبور باید حداقل ۸ کاراکتر باشد.")

        return password

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")

        if not phone.isdigit():
            raise ValidationError("شماره تلفن فقط باید شامل ارقام باشد.")

        if not phone.startswith("09"):
            raise ValidationError("شماره تلفن باید با 09 شروع شود.")

        return phone


class CheckOtpform(forms.ModelForm):
    code = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "w-full drop-shadow-lg outline-none rounded-2xl py-2 text-center"
            }
        ),
        max_length=4,
    )

    def clean_code(self):
        code = self.cleaned_data.get("code")

        if not code:
            raise ValidationError("لطفاً کد تأیید را وارد کنید.")

        if not code.isdigit():
            raise ValidationError("کد باید فقط شامل ارقام باشد.")

        if len(code) != 4:
            raise ValidationError("کد باید دقیقاً ۴ رقم باشد.")

        return code

    class Meta:
        model = Otp
        fields = ["code"]


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "input_second input_all", "placeholder": "رمز عبور فعلی"}
        )
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "input_second input_all", "placeholder": "رمز عبور جدید"}
        )
    )
    confirm_new_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "input_second input_all",
                "placeholder": "تکرار رمز عبور جدید",
            }
        )
    )

    def clean_new_password(self):
        new_password = self.cleaned_data.get("new_password")
        if len(new_password) < 8:
            raise ValidationError("رمز عبور باید حداقل 8 کاراکتر باشد.")
        if len(new_password) > 20:
            raise ValidationError("رمز عبور نباید بیشتر از 20 کاراکتر باشد.")
        return new_password

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_new_password = cleaned_data.get("confirm_new_password")

        if (
            new_password
            and confirm_new_password
            and new_password != confirm_new_password
        ):
            raise ValidationError("رمز عبور جدید و تکرار آن مطابقت ندارند.")
        return cleaned_data
