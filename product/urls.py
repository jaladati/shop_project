from django.urls import path, re_path

from product.views import ProductListView, product_list_filter, ProductDetailView

app_name = "product"

urlpatterns = [
    path("", ProductListView.as_view(), name="list"),
    path("filter/", product_list_filter, name="filter"),
    re_path(r"(?P<slug>[-\w0-9]+)/$", ProductDetailView.as_view(), name="detail"),
]