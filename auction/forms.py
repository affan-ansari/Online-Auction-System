from datetime import datetime
from django import forms
from .models import Bid, Product, Auction


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput(
            attrs={'accept': 'image/*'}))
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class ProductCreateForm(forms.ModelForm):
    images = MultipleFileField(label="Images", required=False)

    class Meta:
        model = Product
        exclude = ['seller', 'status']


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


class BidCreateForm(forms.ModelForm):
    class Meta:
        model = Bid
        exclude = ['buyer', 'is_winning_bid']


class BidUpdateForm(forms.ModelForm):
    class Meta:
        model = Bid
        exclude = ['buyer', 'is_winning_bid', 'product']


class FileFieldForm(forms.Form):
    file_field = MultipleFileField(label="Images", required=False)
