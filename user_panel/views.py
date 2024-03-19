from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import UpdateView
from django.views.decorators.http import require_GET
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.core.paginator import (
    Paginator,
    PageNotAnInteger,
    EmptyPage
)

from account import models
from cart.models import Cart
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

    def get_object(self, queryset=...):
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
                login(request, user)
                messages.success(request, "گذرواژه شما با موفقیت تغییر یافت")
                return redirect(reverse("user_panel:dashboard"))
            else:
                form.add_error("current_password", "گذرواژه نادرست است.")

        return render(request, "user_panel/change_password.html", context)


@require_GET
@login_required
def lists(request):
    """User lists page"""
    # TODO: add user's custom lists.
    return render(request, "user_panel/lists.html")


def base_product_list_filter(request, list_title):
    # Get user.
    user = request.user
    if list_title == "لیست آرزو":
        # Get the user's wish list products.
        products = user.liked_products.all()
    else:
        # TODO: get the list from custom lists of user.
        products = user.liked_products.all()

    # Paginate based on user selection.
    paginate_by = request.GET.get("paginate_by", "10")
    if paginate_by not in ["5", "10", "15"]:
        paginate_by = 10

    # Create the paginator object.
    paginator = Paginator(products, paginate_by)

    # Get the page number.
    page = request.GET.get("page", 1)

    # Get the selected page.
    try:
        page_obj = paginator.get_page(page)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)

    return page_obj, paginate_by


@require_GET
@login_required
def list_detail(request, list_title):
    page_obj, _ = base_product_list_filter(request, list_title)
    context = {
        "page_obj": page_obj,
        "list_title": list_title
    }
    return render(request, "user_panel/list_detail.html", context)


@require_GET
@login_required
def products_list_filter(request) -> JsonResponse:
    """Filter the product list with ajax"""
    list_title = request.GET.get("list_name")
    page_obj, paginate_by = base_product_list_filter(
        request, list_title)

    data = {}
    products_filter_url = reverse("user_panel:filter")
    if request.GET.get("paginate_change") == "true":
        data["paginates"] = render_to_string(
            "components/paginate.html", {"paginate_by": paginate_by, "products_filter_url": products_filter_url})
    data["products"] = render_to_string(
        "includes/products_partial.html", {"products": page_obj.object_list}, request)
    data["pagination"] = render_to_string(
        "components/paging.html", {"page_obj": page_obj, "products_filter_url": products_filter_url})

    return JsonResponse(data)


@require_GET
@login_required
def cart(request):
    user = request.user
    cart, _ = Cart.objects.prefetch_related(
        "items").get_or_create(user=user, is_paid=False)

    context = {
        "cart": cart
    }
    return render(request, "user_panel/cart.html", context)
