import random
import string
import datetime

from django.views.generic import View
from django.shortcuts import render
from django.http import Http404
from django.utils.crypto import get_random_string

from utils.email_service import send_email
from .models import User
from .forms import RegisterForm


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

            send_email("فعال سازی حساب کاربری", user.email, {"email_activate_code":user.email_activate_code}, "emails/register_account.html")
            
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
                return render(request, "account/activate_account.html")
        raise Http404()
