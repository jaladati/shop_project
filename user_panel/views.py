from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import UpdateView
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages

from account import models
from . import forms


@method_decorator(login_required, "dispatch")
class DashboardView(View):
    def get(self, request):
        context = {
            "user": request.user
        }
        return render(request, "user_panel/dashboard.html", context)


@method_decorator(login_required, "dispatch")
class EditProfileView(UpdateView):
    model = models.User
    form_class = forms.EditProfileForm
    template_name = "user_panel/edit_profile.html"
    success_url = reverse_lazy("user_panel:dashboard")

    def get_object(self, queryset = ...):
        user: models.User = self.request.user
        return self.model.objects.get(is_active=True, id=user.id)
    
    def form_valid(self, form) -> HttpResponse:
        messages.success(self.request, "اطلاعات شما با موفقیت تغییر یافت")
        return super().form_valid(form)


@login_required
def change_password(request):
    if request.method == "GET":
        form = forms.ChangePasswordForm()
        return render(request, "user_panel/change_password.html", {"form": form})
    else:
        form = forms.ChangePasswordForm(request.POST)
        context = {
            "form": form
        }
        if form.is_valid():
            cd = form.cleaned_data
            user: models.User = request.user
            if user.check_password(cd["current_password"]):
                user.set_password(cd["password"])
                user.save()
                messages.success(request, "گذرواژه شما با موفقیت تغییر یافت")
                return redirect(reverse("user_panel:dashboard"))
            else:
                form.add_error("current_password", "گذرواژه نادرست است.")

        return render(request, "user_panel/change_password.html", context)
