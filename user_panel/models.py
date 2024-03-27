from django.db import models


class UserProductList(models.Model):
    title = models.CharField(max_length=75, verbose_name="عنوان")
    description = models.TextField(
        blank=True, null=True, verbose_name="توضیحات")
    user = models.ForeignKey(
        to="account.User", on_delete=models.CASCADE, related_name="product_lists", verbose_name="کاربر")
    products = models.ManyToManyField(
        to="product.Product", related_name="user_lists", blank=True, verbose_name="محصولات")

    def __str__(self) -> str:
        return f"{self.user.username}-{self.title}"

    class Meta:
        unique_together = [
            ("user", "title")
        ]
        verbose_name = "لیست محصولات کاربران"
        verbose_name_plural = "لیست های محصولات کاربران"
