from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect

from .forms.forms import SignupForm, UserUpdateForm


def index(request):
    return render(request, 'users/index.html')


def user_signup(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'users/signup.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('index')


@login_required
def user_profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST,
                              request.FILES,
                              instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')

    else:
        form = UserUpdateForm(instance=request.user)

    context = {
        'form': form,
    }

    return render(request, 'users/profile.html', context)
