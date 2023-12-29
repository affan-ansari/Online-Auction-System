from dataclasses import field
from django import forms
from django.contrib.auth.forms import UserCreationForm
from core import settings
from django.contrib.auth import get_user_model

text = '* 123123\n* abcs2312'


class SignupForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'image']
