from django.db import models
from django.utils.text import slugify
from django.db.models import Sum
from django.core.validators import MaxValueValidator, MinValueValidator

from django_jalali.db import models as jmodels
from colorfield.fields import ColorField


# managers
class EnabledManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_enable=True)


class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name="عنوان")
    is_enable = models.BooleanField(default=True, verbose_name="فعال")
    parent = models.ForeignKey(
        to="self", on_delete=models.SET_NULL, null=True, blank=True, related_name="categories", verbose_name="والد")
    slug = models.SlugField(max_length=300, blank=True, verbose_name="اسلاگ")
    image = models.ImageField(
        upload_to="images/categories", null=True, verbose_name="تصویر")

    objects = models.Manager()
    enabled = EnabledManager()

    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs) -> None:
        self.slug = slugify(F"{self.title}-{self.pk}", allow_unicode=True)
        return super().save(*args, **kwargs)


class Product(models.Model):
    title = models.CharField(max_length=255, verbose_name="عنوان")
    slug = models.SlugField(max_length=300, blank=True, verbose_name="اسلاگ")
    is_enable = models.BooleanField(default=True, verbose_name="فعال")

    price = models.PositiveBigIntegerField(verbose_name="قیمت")
    off = models.DecimalField(
        max_digits=5, decimal_places=1, default=0, validators=[MaxValueValidator(100.0), MinValueValidator(0.0)], verbose_name="تخفیف")

    created_time = jmodels.jDateTimeField(
        auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_time = jmodels.jDateTimeField(
        auto_now=True, verbose_name="تاریخ بروزرسانی")

    category = models.ForeignKey(to=Category, null=True, blank=True,
                                 on_delete=models.SET_NULL, related_name="products", verbose_name="دسته بندی")

    description = models.TextField(verbose_name="توضیحات کامل")

    size = models.CharField(max_length=100, null=True,
                            blank=True, verbose_name="اندازه")

    image = models.ImageField(
        upload_to="images/products", verbose_name="تصویر")

    objects = jmodels.jManager()
    enabled = EnabledManager()

    class Meta:
        ordering = ['-created_time', '-updated_time']
        indexes = [
            models.Index(fields=["-created_time"])
        ]
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"

    def __str__(self) -> str:
        return F"{self.title}-{self.price}"

    def save(self, *args, **kwargs) -> None:
        self.slug = slugify(F"{self.title}-{self.pk}", allow_unicode=True)
        return super().save(*args, **kwargs)

    @property
    def stock_count(self):
        return self.color_variants.all().aggregate(Sum("stock_count"))["stock_count__sum"]

    @property
    def final_price(self):
        return int(self.price - self.price * self.off / 100)


class ProductColorVariant(models.Model):
    COLOR_PALETTE = [
        ("#000000", "سیاه"),
        ("#FFFFFF", "سفید"),
        ("#FF0000", "قرمز"),
        ("#0000FF", "آبی"),
        ("#008000", "سبز"),
        ("#FFFF00", "زرد"),
        ("#FFA500", "نارنجی"),
        ("#800080", "بنفش"),
        ("#FFC0CB", "صورتی"),
        ("#964B00", "قهوه ای"),
        ("#808080", "طوسی"),
    ]

    product = models.ForeignKey(to=Product, on_delete=models.CASCADE,
                                related_name="color_variants", verbose_name="محصول")


    color_name = models.CharField(
        max_length=300, verbose_name="نام رنگ")
    color_hex_code = ColorField(
        samples=COLOR_PALETTE, verbose_name="کد hex رنگ")
    stock_count = models.PositiveBigIntegerField(verbose_name="تعداد موجودی")

    class Meta:
        verbose_name = "رنگ"
        verbose_name_plural = "رنگ ها"

    def __str__(self) -> str:
        return F"{self.color_name}-{self.stock_count}"


class ProductGallery(models.Model):
    product = models.ForeignKey(
        to=Product, on_delete=models.CASCADE, related_name="images", verbose_name="محصول")
    image = models.ImageField(
        upload_to="images/products", verbose_name="تصویر")

    class Meta:
        verbose_name = "گالری محصولات"
        verbose_name_plural = "گالری های محصولات"

    def __str__(self) -> str:
        return F"{self.product}"
