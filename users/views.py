from django.contrib.auth import logout
from django.shortcuts import render, redirect

from .forms.forms import SignupForm, LoginForm


def index(request):
    return render(request, 'users/index.html')


def user_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'users/signup.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('index')
