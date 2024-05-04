from django.shortcuts import render
from django.views.generic import View
from django.contrib import messages
from .forms import TicketForm


class ContactUsView(View):
    def get(self, request):
        user = request.user
        initial = {}
        if user.is_authenticated:
            initial["email"] = user.email
            initial["name"] = user.get_full_name()
        ticket_form = TicketForm(initial=initial)
        return render(request, "contact_us/contact.html", {"form": ticket_form})

    def post(self, request):
        ticket_form = TicketForm(request.POST)
        if ticket_form.is_valid():
            ticket_form.save()
            messages.success(
                request, "پیام شما با موفقیت ارسال شد")
            ticket_form = TicketForm()
        return render(request, "contact_us/contact.html", {"form": ticket_form})
