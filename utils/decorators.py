from django.shortcuts import redirect
from django.urls import reverse


def logout_required(func):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse("home:index"))
        return func(request, *args, **kwargs)
    return wrap
