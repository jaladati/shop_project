from django.shortcuts import render
from django.views.generic import TemplateView

from product.models import Category, Product


def index(request):
    context = {
        "categories": Category.enabled.all(),
        "products": Product.enabled.all(),
    }
    return render(request, "index.html", context)


class HeaderComponentView(TemplateView):
    template_name = "components/header.html"


class FooterComponentView(TemplateView):
    template_name = "components/footer.html"
