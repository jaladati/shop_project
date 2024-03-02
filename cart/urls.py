from django.urls import path
from . import views

app_name = "cart"

urlpatterns = [
    path("add-product-to-cart/", views.add_product_to_cart,
         name="add_product_to_cart"),
    path("remove-product-from-cart/", views.remove_product_from_cart,
         name="remove_product_from_cart"),
]
