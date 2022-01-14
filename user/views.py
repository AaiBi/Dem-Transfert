from datetime import date
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404

from user.forms import EditUserPasswordForm, EditUserInfoForm


def login_user(request):
    if request.method == 'GET':
        return render(request, 'user/profile/login_user.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'user/profile/login_user.html', {'form': AuthenticationForm(), 'error': 'Votre nom d\'utilisateur et mot de passe ne correspondent pas !'})
        else:
            login(request, user)
            return redirect('profile')


@login_required
def profile(request):
    form = EditUserInfoForm(instance=request.user)

    if 'save_form' in request.POST:
        if request.method == 'POST':
            form = EditUserInfoForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Vos informations ont été modifiées !')
                return redirect('profile')
        else:
            form = EditUserInfoForm(instance=request.user)

    return render(request, 'user/profile/profile.html',{'form': form})

@login_required
def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login_user')


@login_required
def user_password_change(request):
    if request.method == 'POST':
        form = EditUserPasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, f'Votre mot de passe a été modifié avec succès !')
            return redirect('profile')
    else:
        form = EditUserPasswordForm(request.user)
    return render(request, 'user/profile/user_password_change.html', {'form': form})