from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import UpdateView
from django.views.decorators.http import require_GET, require_POST
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.http import Http404, HttpResponse, JsonResponse
from django.contrib import messages
from django.core.paginator import (
    Paginator,
    PageNotAnInteger,
    EmptyPage
)

from account import models
from cart.models import Cart
from product.models import Product
from .models import UserProductList
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
        user = self.request.user
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
    user = request.user
    lists = UserProductList.objects.filter(user=user)
    form = forms.UserProductListForm()

    context = {
        "lists": lists,
        "list_creation_form": form
    }

    return render(request, "user_panel/lists.html", context)


def base_product_list_filter(request, list_title):
    # Get user.
    user = request.user
    list = None
    if list_title == "لیست آرزو":
        # Get the user's wish list products.
        products = user.liked_products.all()
    else:
        list = get_object_or_404(UserProductList, user=user, title=list_title)
        products = list.products.all()

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

    return page_obj, paginate_by, list


@require_GET
@login_required
def list_detail(request, list_title):
    page_obj, _, list = base_product_list_filter(request, list_title)
    edit_list_form = forms.UserProductListForm(instance=list)

    if not list:
        list = {
            "title": "لیست آرزو",
            "description": "محصولاتی که پسندیده بوده اید را می توانید در اینجا مشاهده کنید."
        }

    context = {
        "page_obj": page_obj,
        "edit_list_form": edit_list_form,
        "list": list
    }
    return render(request, "user_panel/list_detail.html", context)


@require_GET
@login_required
def products_list_filter(request) -> JsonResponse:
    """Filter the products of user list with ajax"""
    list_title = request.GET.get("list_name")
    page_obj, paginate_by, _ = base_product_list_filter(
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


@require_POST
@login_required
def create_list(request) -> JsonResponse:
    """Create user list with ajax."""
    # Fill the list creation form.
    form = forms.UserProductListForm(request.POST)
    context = {}
    if form.is_valid():
        user = request.user
        list = form.save(commit=False)
        list.user = user
        # Is there a list for this user with the same title?
        if UserProductList.objects.filter(user=user, title=list.title).exists():
            form.add_error("title", "لیستی با این عنوان از قبل وجود دارد.")
            context["form"] = render_to_string(
                "components/list_creation_form.html", {"form": form})
        else:
            list.user = user
            # Save the list in database.
            list.save()
            lists = UserProductList.objects.filter(user=request.user)
            context["user_lists"] = render_to_string(
                "includes/lists_partial.html", {"lists": lists}, request)
    else:
        context["form"] = render_to_string(
            "components/list_creation_form.html", {"form": form})
    return JsonResponse(context)


@require_GET
@login_required
def edit_list(request):
    """Edit user lists with ajax."""
    try:
        list_id = int(request.GET.get("id"))
    except:
        response = {
            "text": "خطایی رخ داد",
            "icon": "error",
            "position": "center"
        }
        return JsonResponse(response)

    user = request.user
    # Find the current user list.
    list = get_object_or_404(UserProductList, id=list_id, user_id=user.id)
    current_list_title = list.title
    # Fill the edit list form.
    form = forms.UserProductListForm(request.GET, instance=list)
    context = {}
    if form.is_valid():
        new_list = form.save(commit=False)
        # If the title has changed, check its uniqueness.
        if new_list.title != current_list_title \
                and UserProductList.objects.filter(user=user, title=new_list.title).exists():
            form.add_error("title", "لیستی با این عنوان از قبل وجود دارد")
            context["form"] = render_to_string(
                "components/list_creation_form.html", {"form": form})
        else:
            # Save the changes in database.
            new_list.save()
    else:
        context["form"] = render_to_string(
            "components/list_creation_form.html", {"form": form})
    return JsonResponse(context)


@require_GET
@login_required
def remove_list(request) -> JsonResponse:
    """remove user list with ajax."""
    try:
        id = int(request.GET.get("id"))
    except:
        response = {
            "text": "خطایی رخ داد", "icon": "error", "position": "center"
        }
        return JsonResponse(response)
    # Find the user's selected list.
    list = UserProductList.objects.filter(
        user_id=request.user.id, id=id).first()
    # Return error if the list isn't found.
    if list is None:
        response = {
            "text": "لیست یافت نشد", "icon": "error", "position": "center"
        }
        return JsonResponse(response)

    # Delete the user list from the database.
    list.delete()

    response = {
        "text": "لیست حذف شد", "icon": "success", "position": "center"
    }
    return JsonResponse(response)


@require_GET
@login_required
def add_product_to_list(request) -> JsonResponse:
    """Add product to user list with ajax"""
    # Try to get the list id and product id.
    try:
        list_id = int(request.GET.get("list_id"))
        product_id = int(request.GET.get("product_id"))
    # Return error if the type of list id or product id is incorrect.
    except:
        response = {
            "text": "خطایی رخ داد",
            "icon": "error",
            "position": "center"
        }
        return JsonResponse(response)

    user = request.user

    # Get the products that this user can access.
    products = Product.access_controlled.filter_queryset_by_user_perms(user)

    # Find the selected product.
    product = products.filter(id=product_id).first()

    # Return error if product not found.
    if product is None:
        response = {
            "text": "محصول یافت نشد",
            "icon": "error",
            "positino": "center"
        }
        return JsonResponse(response)

    # Find the selected list.
    list = UserProductList.objects.filter(user=user, id=list_id).first()

    # Return error if list not found.
    if list is None:
        response = {
            "text": "لیست یافت نشد",
            "icon": "error",
            "positino": "center"
        }
        return JsonResponse(response)

    # Add product to list.
    list.products.add(product)

    response = {
        "text": "محصول با موفقیت به لیست شما اضافه شد",
        "icon": "success",
        "position": "center"
    }
    return JsonResponse(response)


@require_GET
@login_required
def remove_product_from_list(request) -> JsonResponse:
    """Remove the product from user list with ajax"""
    # Try to get the list id and product id.
    try:
        list_id = int(request.GET.get("list_id"))
        product_id = int(request.GET.get("product_id"))
    # Return error if the type of list id or product id is incorrect.
    except:
        response = {
            "error": "خطایی رخ داد",
        }
        return JsonResponse(response)

    # Try to get the selected product.
    try:
        product = Product.objects.get(id=product_id)
    # Return error if the product not found.
    except:
        response = {
            "error": "محصول یافت نشد"
        }
        return JsonResponse(response)

    # Try to get the user list.
    try:
        list = UserProductList.objects.get(user=request.user, id=list_id)
    # Return error if the list not found.
    except:
        response = {
            "error": "لیست یافت نشد"
        }
        return JsonResponse(response)

    # Remove the product from list.
    list.products.remove(product)

    response = {
        "status": "removed"
    }
    return JsonResponse(response)


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


@require_GET
@login_required
def orders(request):
    """User orders page"""
    user = request.user
    paid_carts = user.carts.filter(is_paid=True)

    return render(request, "user_panel/orders.html", {"orders": paid_carts})


@require_GET
@login_required
def order_detail(request, order_id):
    """User order details page"""
    user = request.user
    # Find the selected order.
    order = user.carts.filter(is_paid=True, id=order_id).first()
    # Return error if the order isn't found.
    if order is None:
        return Http404("سفارش یافت نشد")

    return render(request, "user_panel/order_detail.html", {"order": order})
