from django.shortcuts import render
from django.views.generic import TemplateView

from product.models import Category, Product


def index(request):
    categories = list(reversed(Category.enabled.all()))
    context = {
        "categories": categories,
        "products": Product.enabled.all(),
    }
    return render(request, "index.html", context)


class HeaderComponentView(TemplateView):
    template_name = "components/header.html"


class FooterComponentView(TemplateView):
    template_name = "components/footer.html"
