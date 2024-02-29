from django.urls import path
from . import views

app_name = "cart"

urlpatterns = [
    path("add-product-to-cart/", views.add_product_to_cart, name="add_product_to_cart"),
]
