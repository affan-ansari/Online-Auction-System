from dataclasses import field
from django import forms
from django.contrib.auth.forms import UserCreationForm
from core import settings
from django.contrib.auth import get_user_model

from users.models import User

text = '* 123123\n* abcs2312'


class SignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['user_type'].choices = [
            ('Buyer', 'Buyer'),
            ('Seller', 'Seller'),
        ]

    email = forms.EmailField()

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password1', 'password2', 'user_type']


class UserUpdateForm(forms.ModelForm):

    email = forms.EmailField()

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'image', 'user_type']

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['user_type'].choices = [
            ('Buyer', 'Buyer'),
            ('Seller', 'Seller'),
        ]
