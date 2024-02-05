from django.urls import path

from .views import (
    RegisterView,
    ActivateAccountView,
    LoginView,
    LogoutView,
    ForgetPasswordView,
    ResetPasswordView,
)

app_name = "account"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("activate-account/<str:email_activate_code>/", ActivateAccountView.as_view(), name="activate_account"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("forget-password", ForgetPasswordView.as_view(), name="forget_password"),
    path("reset-password/<str:activate_code>/", ResetPasswordView.as_view(), name="reset_password"),
]
