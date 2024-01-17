from typing import Any
from django.http import HttpRequest, JsonResponse, BadHeaderError
from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.decorators.http import require_GET
from django.template.loader import render_to_string

from operator import attrgetter

from .models import Product, Category


class ProductListView(ListView):
    queryset = Product.enabled.all()
    paginate_by = 10
    template_name = "product/product_list.html"
    context_object_name = "products"
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        db_categories = Category.objects.all()
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

    db_categories = Category.objects.all()
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

        products = sorted(categories[0].get_products(), key=attrgetter(ordering.replace("-","")))
        if "-" in ordering:
            products.reverse()

        categories = reversed(categories)
    else:
        products = Product.objects.order_by(ordering)
        categories = db_categories.filter(parent=None)
    
    db_max_price = sorted(products, key=lambda product: product.final_price, reverse=True)[0].final_price

    start_price = int(request.GET.get("start_price", 0))
    end_price = int(request.GET.get("end_price", db_max_price))


    products = list(filter(lambda product: end_price >= product.final_price >= start_price, products))

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
