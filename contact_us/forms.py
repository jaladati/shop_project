from django import forms
from .models import Ticket


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        exclude = ["read_by_admin", "admin_answer"]
        widgets = {
            "subject": forms.Select(choices=Ticket.Subject.choices, attrs={
                "class": "form-control"
            }),
            "message": forms.Textarea(attrs={
                "class": "form-control", "placeholder": "پیام", "onfocus": "this.placeholder = ''", "onblur": "this.placeholder = 'پیام'", "required": "true"
            }),
            "name": forms.TextInput(attrs={
                "class": "form-control", "placeholder": "نام و نام خانوادگی", "onfocus": "this.placeholder = ''", "onblur": "this.placeholder = 'نام و نام خانوادگی'"
            }),
            "phone": forms.TextInput(attrs={
                "class": "form-control", "placeholder": "شماره تماس", "onfocus": "this.placeholder = ''", "onblur": "this.placeholder = 'شماره تماس'"
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control", "placeholder": "ایمیل", "onfocus": "this.placeholder = ''", "onblur": "this.placeholder = 'ایمیل'"
            })
        }

