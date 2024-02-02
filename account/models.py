from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    avatar = models.ImageField(
        upload_to="images/profiles", default="images/profiles/default-avatar.png", blank=True, verbose_name="آواتار")
    email = models.EmailField("ایمیل", unique=True)
    email_activate_code = models.CharField(
        max_length=100, verbose_name="کد فعالسازی ایمیل")
    is_active = models.BooleanField(default=False, verbose_name="فعال")
    address = models.TextField(verbose_name="آدرس", blank=True, null=True)

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"

    def __str__(self) -> str:
        return self.get_full_name() if self.get_full_name() else self.username
