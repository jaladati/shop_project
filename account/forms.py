from django import forms

from django.contrib.auth.password_validation import validate_password

from .models import User


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(
        max_length=128, required=True, validators=[validate_password]
    )
    confirm_password = forms.CharField(
        max_length=128, required=True
    )

    def clean_email(self):
        email = self.cleaned_data["email"]
        if not User.objects.filter(email=email).exists():
            return email

        raise forms.ValidationError("کاربری با این ایمیل از قبل وجود دارد.")

    def clean_confirm_password(self):
        password = self.data["password"]
        confirm_password = self.data["confirm_password"]

        if password == confirm_password:
            return confirm_password

        raise forms.ValidationError("با گذرواژه همخوانی ندارد")


class LoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(max_length=128, required=True)


class ForgetPasswordForm(forms.Form):
    email = forms.EmailField(
        required=True, label="ایمیل", widget=forms.EmailInput(attrs={
            "class": "form-control", "dir": "rtl"
        })
    )


class ResetPasswordForm(forms.Form):
    password = forms.CharField(
        max_length=128, required=True, validators=[validate_password],
        widget=forms.PasswordInput(attrs={
            "class": "form-control", "dir": "rtl",  "placeholder": "گذرواژه جدید", 'onfocus': "this.placeholder = ''", 'onblur': "this.placeholder = 'گذرواژه جدید'"
        })
    )
    confirm_password = forms.CharField(
        max_length=128, required=True,
        widget=forms.PasswordInput(attrs={
            "class": "form-control", "dir": "rtl",  "placeholder": "تکرار گذرواژه جدید", 'onfocus': "this.placeholder = ''", 'onblur': "this.placeholder = 'تکرار گذرواژه'"
        })
    )

    def clean_confirm_password(self):
        password = self.data["password"]
        confirm_password = self.data["confirm_password"]

        if password == confirm_password:
            return confirm_password

        raise forms.ValidationError("با گذرواژه همخوانی ندارد")
