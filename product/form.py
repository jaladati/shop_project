from django import forms

from .models import ProductComment

class ProductCommentForm(forms.ModelForm):
    class Meta:
        model = ProductComment
        fields = ["text"]
        labels = {
            "text": ""
        }
        widgets = {
            "text": forms.Textarea(attrs={
                "class": "form-control", "placeholder": "نظر", "id": "commentText"})
        }
