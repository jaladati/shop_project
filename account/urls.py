from django.urls import path

from .views import *

app_name = "account"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("activate-account/<str:email_activate_code>/", ActivateAccountView.as_view(), name="activate_account"),
]
