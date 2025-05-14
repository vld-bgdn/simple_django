from django import forms
from django.core.exceptions import ValidationError
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ("name", "description", "price", "category")
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }

    def clean_name(self):
        name = self.cleaned_data["name"]
        if len(name) < 5:
            raise ValidationError("The name must be more than 5 characters")
        return name
