from django import forms
from django.contrib.auth.password_validation import validate_password

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


class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(
        max_length=128, required=True, label="گذرواژه فعلی",
        widget=forms.PasswordInput(attrs={
            "class": "form-control", "dir": "rtl"
        })
    )
    password = forms.CharField(
        max_length=128, required=True, label="گذرواژه جدید", validators=[validate_password],
        widget=forms.PasswordInput(attrs={
            "class": "form-control", "dir": "rtl"
        })
    )
    confirm_password = forms.CharField(
        max_length=128, required=True, label="تکرار گذرواژه جدید",
        widget=forms.PasswordInput(attrs={
            "class": "form-control", "dir": "rtl"
        })
    )

    def clean_confirm_password(self):
        password = self.data["password"]
        confirm_password = self.data["confirm_password"]

        if password == confirm_password:
            return confirm_password
        raise forms.ValidationError("با گذرواژه جدید همخوانی ندارد")
