from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):

    def create_user(
        self,
        phone,
        password=None,
        first_name="",
        last_name="",
        **extra_fields
    ):
        if not phone:
            raise ValueError("لطفا شماره تلفن را وارد کنید")

        user = self.model(
            phone=phone,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(
        self,
        phone,
        password=None,
        **extra_fields
    ):
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(
            phone=phone,
            password=password,
            **extra_fields
        )