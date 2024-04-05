from django.urls import path

from . import views


app_name = 'user_panel'

urlpatterns = [
    path("", views.DashboardView.as_view(), name="dashboard"),
    path("edit-profile/", views.EditProfileView.as_view(), name="edit_profile"),
    path("change-password/", views.change_password, name="change_password"),
    path("lists/", views.lists, name="lists"),
    path("lists/create-list/", views.create_list, name="create_list"),
    path("lists/edit-list/", views.edit_list, name="edit_list"),
    path("lists/remove-list/", views.remove_list, name="remove_list"),
    path("lists/filter/", views.products_list_filter, name="filter"),
    path("lists/<str:list_title>/", views.list_detail, name="list_detail"),
    path("cart/", views.cart, name="cart")
]
