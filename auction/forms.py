from datetime import datetime
from django import forms
from .models import Product, Auction


class ProductCreateForm(forms.ModelForm):

    class Meta:
        model = Product
        exclude = ['seller', 'is_sold']


class ProductUpdateForm(forms.ModelForm):

    class Meta:
        model = Product
        exclude = ['seller', 'is_sold']


class AucionBaseForm(forms.ModelForm):
    start_time = forms.DateTimeField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            },
        ),
    )
    end_time = forms.DateTimeField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            },
        ),
    )

    class Meta:
        model = Auction
        exclude = ['seller', 'unsold_product_ids']


class AuctionCreateForm(AucionBaseForm):
    pass


class AuctionUpdateForm(AucionBaseForm):
    pass
