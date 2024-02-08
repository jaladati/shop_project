from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


@method_decorator(login_required, "dispatch")
class DashboardView(View):
    def get(self, request):
        context = {
            "user": request.user
        }
        return render(request, "user_panel/dashboard.html", context)
