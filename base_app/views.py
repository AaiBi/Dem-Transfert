from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages


def index(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return render(request, 'base_app/index.html')
        else:
            messages.error(request, 'Veuillez vous connectez pour pouvoir faire cette action !')
            return redirect('login_user')
    #return render(request, 'base_app/index.html', {'reviews': reviews})