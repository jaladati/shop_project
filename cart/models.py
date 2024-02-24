from django.db import models
from django_jalali.db import models as jmodels

from account.models import User
from product.models import ProductColorVariant


class Cart(models.Model):
    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="carts", verbose_name="کاربر")
    first_name = models.CharField(max_length=150, blank=True, null=True, verbose_name="نام")
    last_name = models.CharField(max_length=150, blank=True, null=True, verbose_name="نام خانوادگی")
    phone = models.CharField(max_length=11, blank=True, null=True, verbose_name="تلفن")
    postal_code = models.CharField(max_length=10, blank=True, null=True, verbose_name="کد پستی")
    address = models.TextField(blank=True, null=True, verbose_name="آدرس")
    is_paid = models.BooleanField(default=False, verbose_name="پرداخت شده/نشده")
    payment_date = jmodels.jDateTimeField(blank=True, null=True, verbose_name="تاریخ پرداخت")

    objects = jmodels.jManager()

    def total_price(self) -> int:
        """
        Calculates the total price of cart items based on their paid or current price,
        depending on the payment status.
        """
        total = 0
        if self.is_paid:
            for item in self.items.all():
                total += item.paid_price * item.quantity
        else:
            for item in self.items.all():
                total += item.product.final_price * item.quantity
        return total

    def __str__(self) -> str:
        return F"{self.user}-cart-{self.pk}"

    class Meta:
        verbose_name = "سبد خرید"
        verbose_name_plural = "سبد های خرید"


class CartItem(models.Model):
    cart = models.ForeignKey(
        to=Cart, on_delete=models.CASCADE, related_name="items", verbose_name="سبد خرید")
    product = models.ForeignKey(
        to=ProductColorVariant, on_delete=models.CASCADE, related_name="carts", verbose_name="محصول")
    quantity = models.PositiveIntegerField(verbose_name="تعداد")
    paid_price = models.PositiveBigIntegerField(blank=True, null=True, verbose_name="قیمت پرداخت شده")

    def total_price(self) -> int:
        return self.quantity * (self.paid_price or self.product.final_price)

    def __str__(self) -> str:
        return F"{self.product.product}-{self.cart}"

    class Meta:
        verbose_name = "محصول سبد خرید"
        verbose_name_plural = "محصولات سبد خرید"
