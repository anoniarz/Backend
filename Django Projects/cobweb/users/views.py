from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import user_passes_test

import re


@user_passes_test(lambda u: not u.is_authenticated, login_url='home')
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        page = request.META.get('HTTP_REFERER')
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, 'You have successfully logged in.')
                return redirect(page)
            else:
                messages.error(request, 'Your account is not active.')
                return redirect(page)
        else:
            messages.warning(request, 'Invalid username or password.')
            return redirect(page)



def register(request):
    page = request.META.get('HTTP_REFERER')
    app_name = re.findall(r"/([a-z]{3,})", page)
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if not all([username,email,password1,password2]):
            messages.warning(request, 'Incomplete data')
            return redirect(page)

        if password1 != password2 or not password1:
            messages.warning(request, 'Passwords do not match')
            return redirect(page)

        user = User.objects.create_user(
            username, email=email, password=password1)
        login(request, user)
        messages.success(
            request, 'Registration successful. You are now logged in.')
        if app_name:
            return redirect(f'{app_name[0]}_home')
        else:
            return redirect('home')

    return redirect(page)


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out")
    page = request.META.get('HTTP_REFERER')
    app_name = re.findall(r"/([a-z]{3,})", page)
    if app_name:
        return redirect(f'{app_name[0]}_home')
    else:
        return redirect('home')


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)
