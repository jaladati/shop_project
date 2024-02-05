from django.shortcuts import (
    get_object_or_404,
    render,
)
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_GET
from django.views.generic import (
    ListView,
    DetailView,
)
from django.core.paginator import (
    Paginator,
    PageNotAnInteger,
    EmptyPage,
)
from operator import attrgetter
from typing import Any

from .forms import ProductCommentForm
from .models import (
    Product,
    Category,
    ProductComment,
)


class ProductListView(ListView):
    queryset = Product.enabled.all()
    paginate_by = 10
    template_name = "product/product_list.html"
    context_object_name = "products"
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        db_categories = Category.enabled.all()
        ordering = self.get_ordering()
        category = self.request.GET.get("category")

        if category:
            category = get_object_or_404(db_categories, slug=category)
            categories = [category]
            while True:
                if category.parent is not None:
                    categories.append(category.parent)
                    category = category.parent
                else:
                    break
            products = sorted(categories[0].get_products(), key=attrgetter(ordering.replace("-","")))
            if "-" in ordering:
                products.reverse()

            categories.reverse()
        else:
            products = self.queryset.order_by(self.get_ordering())
            categories = db_categories.filter(parent=None)

        if products:
            db_max_price = sorted(products, key=lambda product: product.final_price, reverse=True)[0].final_price
            try:
                start_price = int(self.request.GET.get("start_price", 0))
                end_price = int(self.request.GET.get("end_price", db_max_price))
            except:
                start_price = 0
                end_price = db_max_price
            else:
                products = list(filter(lambda product: end_price >= product.final_price >= start_price, products))
                if self.request.GET.get("in_stock") == "true":
                    products = list(filter(lambda product: product.stock_count, products))

        context["categories"] = categories
        context["page_obj"] = self.paginate_queryset(products, self.get_paginate_by(products))[1]
        context["start_price"] = start_price
        context["end_price"] = end_price
        context["db_max_price"] = db_max_price
        
        return context

    def get_paginate_by(self, queryset) -> int | None:
        paginate_by = self.request.GET.get("paginate_by")

        if paginate_by not in ["5", "10", "15"]:
            paginate_by = self.paginate_by

        return paginate_by

    def get_ordering(self):
        order_num = self.request.GET.get("sort")
        match order_num:
            case "most-expensive":
                ordering = "-price"
            case "cheapest":
                ordering = "price"
            case "newest" | _:
                ordering = "-created_time"
        return ordering

@require_GET
def product_list_filter(request: HttpRequest):
    order_num = request.GET.get("sort")
    match order_num:
        case "most-expensive":
            ordering = "-price"
        case "cheapest":
            ordering = "price"
        case "newest" | _:
            ordering = "-created_time"

    db_categories = Category.enabled.all()
    category = request.GET.get("category")

    if category:
        category = get_object_or_404(db_categories, slug=category)
        categories = [category]
        while True:
            if category.parent is not None:
                categories.append(category.parent)
                category = category.parent
            else:
                break
        products = categories[0].get_products()
        products = filter(lambda product: product.is_enable, products)
        products = sorted(categories[0].get_products(), key=attrgetter(ordering.replace("-","")))
        if "-" in ordering:
            products.reverse()

        categories = reversed(categories)
    else:
        products = Product.objects.filter(is_enable=True).order_by(ordering)
        categories = db_categories.filter(parent=None)
    

    db_max_price = sorted(products, key=lambda product: product.final_price, reverse=True)[0].final_price

    start_price = int(request.GET.get("start_price", 0))
    end_price = int(request.GET.get("end_price", db_max_price))


    products = list(filter(lambda product: end_price >= product.final_price >= start_price, products))

    if request.GET.get("in_stock") == "true":
        products = list(filter(lambda product: product.stock_count, products))

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
    
    data = {}

    if request.GET.get("category_change") == "true":
        data["categories"] = render_to_string("components/category.html", {"categories":categories}, request)
    elif request.GET.get("paginate_change") == "true":
        data["paginates"] = render_to_string("components/paginate.html", {"paginate_by": paginate_by})

    data["products"] = render_to_string("includes/products_partial.html", {"products":page_obj.object_list})
    data["pagination"] = render_to_string("components/paging.html", {"page_obj":page_obj})
    data["price_filter"] = render_to_string("components/price_filter.html")

    return JsonResponse(data)

class ProductDetailView(DetailView):
    template_name = "product/product_detail.html"
    queryset = Product.enabled

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["comments"] = self.get_object().comments.filter(parent=None, is_enable=True).prefetch_related("childs")
        context["form"] = kwargs.get("form", ProductCommentForm())
        return context
    
    @method_decorator(login_required)
    def post(self, request: HttpRequest, slug):
        form = ProductCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = self.get_object()
            comment.user = request.user
            if parent_id := request.POST.get("parent_id"):
                comment.parent = get_object_or_404(ProductComment.enabled, parent=None, id=parent_id)
            comment.save()
            form = ProductCommentForm()
        self.object = self.get_object()
        
        context = self.get_context_data(object=self.object, form=form)
        return render(request, self.template_name, context)
        
