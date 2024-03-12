from django.urls import path, re_path

from product.views import (
    product_list,
    product_list_filter,
    ProductDetailView,
    remove_comment,
    change_comment_status
)

app_name = "product"

urlpatterns = [
    path("", product_list, name="list"),
    path("filter/", product_list_filter, name="filter"),
    path("remove-comment/", remove_comment, name="remove_coment"),
    path("change-comment-status/", change_comment_status, name="change_comment-status"),
    re_path(r"(?P<slug>[-\w0-9]+)/$", ProductDetailView.as_view(), name="detail"),
]