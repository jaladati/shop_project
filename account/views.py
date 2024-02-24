import random
import string
import datetime
from django.urls import reverse, reverse_lazy

from django.views.generic import View
from django.contrib.auth.views import LogoutView
from django.shortcuts import redirect, render
from django.http import Http404, HttpRequest
from django.contrib import messages
from django.utils.crypto import get_random_string
from django.contrib.auth import login
from django.utils.decorators import method_decorator

from utils.email_service import send_email
from utils.decorators import logout_required

from .models import User
from .forms import (
    LoginForm,
    RegisterForm,
    ForgetPasswordForm,
    ResetPasswordForm,
)


@method_decorator(logout_required, "dispatch")
class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, "account/register.html", {"form": form})
    def post(self, request):
        form = RegisterForm(request.POST)
        context = {
            "form": form
        }
        if form.is_valid():
            cd = form.cleaned_data
            user = User()
            while True:
                username = ''.join(random.choices(string.ascii_letters+string.digits, k=20))
                if not User.objects.filter(username=username).exists():
                    break
            user.username = username
            user.set_password(cd["password"])
            user.email = cd["email"]
            user.email_activate_code = get_random_string(99)

            send_email("فعال سازی حساب کاربری", user.email,
                       {"email_activate_code":user.email_activate_code}, "emails/register_account.html")
            user.last_login = datetime.datetime.now(datetime.timezone.utc)
            user.save()
            context["form"] = RegisterForm()
            context["create_account_alert"] = "true"

        return render(request, "account/register.html", context)


class ActivateAccountView(View):
    def get(self, request, email_activate_code):
        user = User.objects.filter(email_activate_code=email_activate_code).first()
        if user is not None:
            now = datetime.datetime.now(datetime.timezone.utc)
            time_difference: datetime.timedelta = now - user.last_login
            if time_difference.total_seconds() < 7200:
                user.is_active = True
                user.email_activate_code = get_random_string(99)
                user.save()
                return render(request, "account/activate_account.html")
        raise Http404()


@method_decorator(logout_required, "dispatch")
class LoginView(View):
    def get(self, request: HttpRequest):
        if request.user.is_authenticated:
            return redirect(reverse("home:index"))
        form = LoginForm()
        context = {
            "form": form,
        }
        return render(request, "account/login.html", context)
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            email = cd["email"]
            password = cd["password"]
            user = User.objects.filter(email=email).first()
            if user is not None and user.check_password(password):
                if user.is_active:
                    login(request, user)
                    messages.success(request, "خوش آمدید")
                    return redirect(reverse("user_panel:dashboard"))
                else:
                    form.add_error("email", "این حساب هنوز فعال نشده است.")
            else:
                form.add_error("email", "کاربری با این مشخصات یافت نشد.")
        context = {
            "form": form
        }
        return render(request, "account/login.html", context)


class LogoutView(LogoutView):
    next_page = reverse_lazy("account:login")


@method_decorator(logout_required, "dispatch")
class ForgetPasswordView(View):
    def get(self, request):
        form = ForgetPasswordForm()
        context = {
            "form": form
        }
        return render(request, "account/forget_password.html", context)
    def post(self, request):
        form = ForgetPasswordForm(request.POST)
        context = {
            "form": form
        }
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.filter(email=cd["email"]).first()
            if user is not None:
                send_email("فراموشی کلمه عبور", user.email,
                           {"activate_code":user.email_activate_code}, "emails/forget_password.html")
                user.last_login = datetime.datetime.now(datetime.timezone.utc)
                user.save()
                context["email_alert"] = "true"
            else:
                form.add_error("email", "کاربری با این ایمیل یافت نشد")
        return render(request, "account/forget_password.html", context)


@method_decorator(logout_required, "dispatch")
class ResetPasswordView(View):
    def get(self, request, activate_code):
        user = User.objects.filter(email_activate_code=activate_code).first()
        if user is not None:
            now = datetime.datetime.now(datetime.timezone.utc)
            time_difference: datetime.timedelta = now - user.last_login
            if time_difference.total_seconds() < 7200:
                form = ResetPasswordForm()
                context = {
                    "form": form,
                }
                return render(request, "account/reset_password.html", context)
        raise Http404()

    def post(self, request, activate_code):
        form = ResetPasswordForm(request.POST)
        context = {
            "form": form,
        }
        if form.is_valid():
            user = User.objects.filter(email_activate_code=activate_code).first()
            if user is None:
                raise Http404()

            now = datetime.datetime.now(datetime.timezone.utc)
            time_difference: datetime.timedelta = now - user.last_login
            if time_difference.total_seconds() > 7200:
                raise Http404()

            cd = form.cleaned_data
            user.is_active = True
            password = cd["password"]
            user.set_password(password)
            user.email_activate_code = get_random_string(99)
            user.save()
            context["password_changed_alert"] = "true"
        return render(request, "account/reset_password.html", context)
