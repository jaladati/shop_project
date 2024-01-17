from django.urls import path

from product.views import ProductListView, product_list_filter

app_name = "product"

urlpatterns = [
    path("", ProductListView.as_view(), name="list"),
    path("filter/", product_list_filter, name="filter"),
]