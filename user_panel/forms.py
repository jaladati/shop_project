from django import forms

from account.models import User


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "avatar", "address"]
        widgets = {
            "username": forms.EmailInput(attrs={
                "class": "common-input", "dir": "rtl"
            }),
            "first_name": forms.TextInput(attrs={
                "class": "common-input", "dir": "rtl"
            }),
            "last_name": forms.TextInput(attrs={
                "class": "common-input", "dir": "rtl"
            }),
            "avatar": forms.FileInput(attrs={
                "class": "common-input", "dir": "rtl"
            }),
            "address": forms.Textarea(attrs={
                "class": "common-input", "dir": "rtl", "rows": 4
            }),
        }
        
