from django.contrib.auth.models import BaseUserManager

# پروفایل ادمین


class UserManager(BaseUserManager):
    def create_user(
        self, phone, password=None, first_name=None, last_name=None, **extra_fields
    ):

        if not phone:
            raise ValueError("لطفا شماره تلفن را وارد کنید")

        user = self.model(phone=phone, password=password, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None):

        user = self.create_user(
            phone,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
