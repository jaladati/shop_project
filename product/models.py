from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name="عنوان")
    is_enable = models.BooleanField(default=True, verbose_name="فعال")
    parent = models.ManyToManyField(
        to="self", null=True, blank=True, related_name="categories", verbose_name="والد")
    slug = models.SlugField(max_length=300, verbose_name="اسلاگ")

    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs) -> None:
        self.slug = slugify(F"{self.title}-{self.id}", allow_unicode=True)
        return super().save(*args, **kwargs)
