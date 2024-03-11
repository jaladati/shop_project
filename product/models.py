from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.db.models import Sum
from django.core.validators import MaxValueValidator, MinValueValidator

from django_jalali.db import models as jmodels
from colorfield.fields import ColorField

from account.models import User


# managers
class EnabledManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_enable=True)


class AccessControlledObjectManager(models.Manager):
    def filter_queryset_by_user_perms(self, user: User):
        """
        Filter and return a queryset of model based on user permissions.

        If the user is a superuser, the user has access to all model objects.
        Otherwise, the user only has access to enabled model objects.
        Require `model.enabled`.
        """
        if user.is_superuser:
            return self.model.objects.all()
        else:
            return self.model.enabled.all()


# models
class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name="عنوان")
    is_enable = models.BooleanField(default=True, verbose_name="فعال")
    parent = models.ForeignKey(
        to="self", on_delete=models.SET_NULL, null=True, blank=True, related_name="childs", verbose_name="والد")
    slug = models.SlugField(max_length=300, blank=True, verbose_name="اسلاگ")
    image = models.ImageField(
        upload_to="images/categories", verbose_name="تصویر")

    objects = models.Manager()
    enabled = EnabledManager()
    access_controlled = AccessControlledObjectManager()

    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"

    def get_products(self) -> models.QuerySet:
        """
        Return all products of this category and it's subcategories.
        """
        def get_categories_id(category):
            ids = []
            ids.append(category.id)
            for sub_category in category.childs.all():
                if sub_category.childs.exists():
                    ids.extend(get_categories_id(sub_category))
                else:
                    ids.append(sub_category.id)
            return ids
        ids = get_categories_id(self)
        products = Product.objects.filter(category_id__in=ids)
        return products

    def get_enable_childs(self) -> list:
        """
        Return all of subcategories that are enable.
        """
        return self.childs.filter(is_enable=True)

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs) -> None:
        if not self.pk:
            super().save(*args, **kwargs)
            self.slug = slugify(F"{self.title}-{self.pk}", allow_unicode=True)
        super().save(*args, **kwargs)


class Product(models.Model):
    title = models.CharField(max_length=255, verbose_name="عنوان")
    slug = models.SlugField(max_length=300, blank=True, verbose_name="اسلاگ")
    is_enable = models.BooleanField(default=True, verbose_name="فعال")

    price = models.PositiveBigIntegerField(verbose_name="قیمت")
    off = models.DecimalField(
        max_digits=5, decimal_places=1, default=0, validators=[MaxValueValidator(100.0), MinValueValidator(0.0)], verbose_name="تخفیف")

    specification = models.JSONField(
        default=dict, blank=True, null=True, verbose_name="مشخصات")

    created_time = jmodels.jDateTimeField(
        auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_time = jmodels.jDateTimeField(
        auto_now=True, verbose_name="تاریخ بروزرسانی")

    category = models.ForeignKey(to=Category, null=True, blank=True,
                                 on_delete=models.SET_NULL, related_name="products", verbose_name="دسته بندی")

    short_description = models.CharField(
        max_length=350, verbose_name="توضیحات کوتاه")
    description = models.TextField(verbose_name="توضیحات کامل")

    image = models.ImageField(
        upload_to="images/products", verbose_name="تصویر")

    objects = jmodels.jManager()
    enabled = EnabledManager()
    access_controlled = AccessControlledObjectManager()

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
        if not self.pk:
            super().save(*args, **kwargs)
            self.slug = slugify(F"{self.title}-{self.pk}", allow_unicode=True)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("product:detail", kwargs={'slug': self.slug})

    def in_stock_color_variants(self):
        return self.color_variants.filter(stock_count__gt=0)

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

    price = models.PositiveBigIntegerField(
        null=True, blank=True, verbose_name="قیمت")
    off = models.DecimalField(
        max_digits=5, decimal_places=1, default=0, validators=[MaxValueValidator(100.0), MinValueValidator(0.0)], verbose_name="تخفیف")

    color_name = models.CharField(
        max_length=300, verbose_name="نام رنگ")
    color_hex_code = ColorField(
        samples=COLOR_PALETTE, verbose_name="کد hex رنگ")
    stock_count = models.PositiveBigIntegerField(verbose_name="تعداد موجودی")

    @property
    def get_price(self):
        return self.price or self.product.price

    @property
    def get_off(self):
        return self.off or self.product.off

    @property
    def final_price(self):
        price = self.get_price
        off = self.get_off
        return int(price - price * off / 100)

    def get_absolute_url(self):
        return self.product.get_absolute_url()

    def __str__(self) -> str:
        return F"{self.color_name}-{self.stock_count}"

    class Meta:
        verbose_name = "رنگ"
        verbose_name_plural = "رنگ ها"


class ProductGallery(models.Model):
    product = models.ForeignKey(
        to=Product, on_delete=models.CASCADE, related_name="images", verbose_name="محصول")
    image = models.ImageField(
        upload_to="images/products", verbose_name="تصویر")

    class Meta:
        verbose_name = "تصویر محصول"
        verbose_name_plural = "تصاویر محصول"

    def __str__(self) -> str:
        return F"img-{self.pk}-{self.product}"


class ProductComment(models.Model):
    product = models.ForeignKey(
        to=Product, on_delete=models.CASCADE, related_name="comments", verbose_name="محصول")
    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="products_comments", verbose_name="کاربر")
    parent = models.ForeignKey(
        to="self", on_delete=models.CASCADE, related_name="childs", limit_choices_to={"parent": None}, blank=True, null=True, verbose_name="والد")

    text = models.TextField(verbose_name="نظر")
    is_enable = models.BooleanField(default=True, verbose_name="فعال")
    created_time = jmodels.jDateTimeField(
        auto_now_add=True, verbose_name="تاریخ ایجاد")

    objects = jmodels.jManager()
    enabled = EnabledManager()
    access_controlled = AccessControlledObjectManager()

    class Meta:
        indexes = [
            models.Index(fields=["-created_time"])
        ]
        verbose_name = "نظر"
        verbose_name_plural = "نظرات"

    def __str__(self) -> str:
        return F"{self.product}-{self.user.username}-{self.pk}"
