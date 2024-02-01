from django.shortcuts import render

from product.models import Category, Product


def index(request):
    categories = list(reversed(Category.enabled.all()))
    context = {
        "categories": categories,
        "products": Product.enabled.all(),
    }
    return render(request, "index.html", context)


def header_component(request):
    return render(request, "components/header.html")

def footer_component(request):
    return render(request, "components/footer.html")
