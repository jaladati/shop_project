from django.shortcuts import render
from django.views.generic import TemplateView


def index(request):
    return render(request, "index.html", {'test': 'it is my index view'})


class HeaderComponentView(TemplateView):
    template_name = "components/header.html"


class FooterComponentView(TemplateView):
    template_name = "components/footer.html"
