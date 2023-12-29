from django import forms
from .models import Product


class ProductCreateForm(forms.ModelForm):

    class Meta:
        model = Product
        exclude = ['seller', 'is_sold']


class ProductUpdateForm(forms.ModelForm):

    class Meta:
        model = Product
        exclude = ['seller', 'is_sold']
