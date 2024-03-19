from django.urls import path

from .views import (
    DashboardView,
    EditProfileView,
    cart,
    change_password,
    lists,
    list_detail,
    products_list_filter
)


app_name = 'user_panel'

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path("edit-profile/", EditProfileView.as_view(), name="edit_profile"),
    path("change-password/", change_password, name="change_password"),
    path("lists/", lists, name="lists"),
    path("lists/filter/", products_list_filter, name="filter"),
    path("lists/<str:list_title>/", list_detail, name="list_detail"),
    path("cart/", cart, name="cart")
]
