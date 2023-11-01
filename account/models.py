from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    avatar = models.ImageField(upload_to="images/profiles", null=True, blank=True, verbose_name="آواتار")
    email_activate_code = models.CharField(max_length=100, verbose_name="کد فعالسازی ایمیل")
    is_active = models.BooleanField(default=False, verbose_name="فعال")
    address = models.TextField(verbose_name="آدرس", blank=True, null=True)
    
    def __str__(self) -> str:
        return self.get_full_name() if self.get_full_name() else self.username