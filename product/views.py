from django.shortcuts import (
    get_object_or_404,
    render,
)
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseForbidden, HttpRequest, JsonResponse
from django.views.decorators.http import require_GET
from django.views.generic import DetailView
from django.core.paginator import (
    Paginator,
    PageNotAnInteger,
    EmptyPage,
)
from typing import Any

from utils.decorators import superuser_required
from .forms import ProductCommentForm
from .models import (
    Product,
    Category,
    ProductComment,
)


def base_product_list_filter(request: HttpRequest) -> dict[str, Any]:
    order_by = request.GET.get("sort")
    match order_by:
        case "most-expensive":
            ordering = "-price"
        case "cheapest":
            ordering = "price"
        case "newest" | _:
            ordering = "-created_time"
    user = request.user
    # Find all categories based on user permissions.
    db_controlled_categories = Category.access_controlled.filter_queryset_by_user_perms(
        user)
    # Find all products based on user permissions.
    db_controlled_products = Product.access_controlled.filter_queryset_by_user_perms(
        user
    )

    category_slug = request.GET.get("category")

    if category_slug:
        # Find the entered category.
        category = db_controlled_categories.filter(slug=category_slug).first()

        categories = []
        while True:
            # Check if the category is accessible to the user.
            if category in db_controlled_categories:
                categories.insert(0, category)
            else:
                raise Http404("دسته بندی یافت نشد.")
            # Check if this category has a parent.
            if (parent := category.parent) is not None:
                category = parent
            else:
                break
        # Get the products of the selected category.
        products = categories[-1].get_products(
            db_controlled_products).order_by(ordering)
    else:
        products = db_controlled_products.order_by(ordering)
        categories = db_controlled_categories.filter(parent=None)

    # Search on products.
    q = request.GET.get("q", "")
    products = products.filter(title__contains=q)

    # Check the product queryset is empty or not.
    if products:
        # Get the most expensive price from filtered products.
        db_max_price = sorted(
            products, key=lambda product: product.final_price, reverse=True)[0].final_price

        try:
            start_price = int(request.GET.get("start_price"))
            end_price = int(request.GET.get("end_price"))
        except:
            start_price = 0
            end_price = db_max_price

        # Filter products based on entered prices.
        products = list(filter(lambda product: end_price >=
                        product.final_price >= start_price, products))

        if request.GET.get("in_stock") == "true":
            products = list(
                filter(lambda product: product.stock_count, products))
    else:
        # Set default prices.
        db_max_price = 1000
        end_price = db_max_price
        start_price = 0

    paginate_by = request.GET.get("paginate_by")

    if paginate_by not in ["5", "10", "15"]:
        paginate_by = 10

    paginator = Paginator(products, paginate_by)
    page = request.GET.get("page", 1)

    try:
        page_obj = paginator.get_page(page)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)

    return {
        "categories": categories, "db_max_price": db_max_price,
        "page_obj": page_obj, "paginate_by": paginate_by,
        "start_price": start_price, "end_price": end_price
    }


@require_GET
def product_list(request):
    context = base_product_list_filter(request)
    return render(request, "product/product_list.html", context)


@require_GET
def product_list_filter(request: HttpRequest) -> JsonResponse:
    """
    Filter the products and return the rendered templates.
    """
    context = base_product_list_filter(request)
    page_obj = context["page_obj"]
    start_price = context["start_price"]
    end_price = context["end_price"]
    db_max_price = context["db_max_price"]

    data = {}

    if request.GET.get("category_change") == "true":
        categories = context["categories"]
        data["categories"] = render_to_string(
            "components/category.html", {"categories": categories}, request)
    elif request.GET.get("paginate_change") == "true":
        paginate_by = context["paginate_by"]
        data["paginates"] = render_to_string(
            "components/paginate.html", {"paginate_by": paginate_by})

    data["products"] = render_to_string(
        "includes/products_partial.html", {"products": page_obj.object_list})
    data["pagination"] = render_to_string(
        "components/paging.html", {"page_obj": page_obj})
    data["price_filter"] = render_to_string("components/price_filter.html", {
                                            "start_price": start_price, "end_price": end_price, "db_max_price": db_max_price})

    return JsonResponse(data)


class ProductDetailView(DetailView):
    template_name = "product/product_detail.html"

    def get_queryset(self):
        """
        Filter and return products based on user permissions.
        """
        user = self.request.user
        return Product.access_controlled.filter_queryset_by_user_perms(user)

    def get_comments_queryset(self):
        """
        Filter and return product comments based on user permissions.
        """
        user = self.request.user
        comments = ProductComment.access_controlled.filter_queryset_by_user_perms(
            user)
        product = self.get_object()
        return comments.filter(product=product)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """
        Overwrite the get_context_data method to include comments list and
        comment form.
        """
        context = super().get_context_data(**kwargs)
        comments = self.get_comments_queryset().filter(parent=None)

        context["comments"] = comments
        context["form"] = kwargs.get("form", ProductCommentForm())
        return context

    @method_decorator(login_required)
    def post(self, request: HttpRequest, slug):
        form = ProductCommentForm(request.POST)
        if form.is_valid():
            # Create new comment instance without saving in database.
            comment = form.save(commit=False)

            # Fill up comment fields.
            comment.product = self.get_object()
            comment.user = request.user
            if parent_id := request.POST.get("parent_id"):
                comments = self.get_comments_queryset()
                comment.parent = get_object_or_404(
                    comments, parent=None, id=parent_id)

            # Save comment in database.
            comment.save()

            # Show success message to user.
            messages.success(request, "نظر شما با موفقیت ثبت شد")

            form = ProductCommentForm()
        self.object = self.get_object()
        context = self.get_context_data(object=self.object, form=form)
        return render(request, self.template_name, context)


@require_GET
@superuser_required(error=HttpResponseForbidden())
def remove_comment(request) -> JsonResponse:
    # Find comment.
    comments = ProductComment.objects.all()
    comment_id = request.GET.get("comment_id")
    comment = comments.filter(id=comment_id).first()
    if comment is not None:
        comment.delete()

        # Find product comments.
        product = comment.product
        comments = comments.filter(product=product, parent=None)
        context = {
            "comments": comments.filter(parent=None)
        }
        comment_list_area = render_to_string(
            "includes/comments.html", context, request)
        data = {
            "comment_list_area": comment_list_area
        }
        return JsonResponse(data)
    else:
        return JsonResponse({"error": "نظری یافت نشد"})


@require_GET
@superuser_required(error=HttpResponseForbidden())
def change_comment_status(request) -> JsonResponse:
    # Find comment.
    comment_id = request.GET.get("comment_id")
    comment = ProductComment.objects.filter(id=comment_id).first()
    if comment is not None:
        # Change comment status.
        if comment.is_enable:
            comment.is_enable = False
            current_status = "غیر فعال"
        else:
            comment.is_enable = True
            current_status = "فعال"

        # Save changes to database.
        comment.save()
        data = {
            "current_status": current_status
        }
        return JsonResponse(data)
    else:
        return JsonResponse({"error": "نظری یافت نشد"})
