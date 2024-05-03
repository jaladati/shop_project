from django.db import models
from django.core.exceptions import ValidationError


class Ticket(models.Model):
    class Subject(models.TextChoices):
        PROPOSAL = "PR", "پیشنهاد"
        CRITICISM = "CR", "انتقاد"
        REPORT = "RP", "گزارش"

    subject = models.CharField(max_length=2, choices=Subject.choices, verbose_name="موضوع")
    message = models.TextField(verbose_name="پیام")
    name = models.CharField(max_length=255, verbose_name="نام و نام خانوادگی")
    phone = models.CharField(max_length=11, verbose_name="تلفن تماس")
    email = models.EmailField(verbose_name="ایمیل", blank=True, null=True)

    read_by_admin = models.BooleanField(default=False, verbose_name="خوانده شده توسط مدیر")
    admin_answer = models.TextField(verbose_name="پاسخ مدیر", null=True, blank=True)


    def __str__(self) -> str:
        return f"{self.subject}-{self.name}"

    class Meta:
        verbose_name = "تیکت"
        verbose_name_plural = "تیکت ها"
