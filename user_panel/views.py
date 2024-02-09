from django.shortcuts import render
from django.views import View
from django.views.generic import UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

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
    success_url = "edit-profile"

    def get_object(self, queryset = ...):
        user = self.request.user
        return self.model.objects.get(is_active=True, id=user.id)
