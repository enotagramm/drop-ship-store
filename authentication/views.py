from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render, redirect

from authentication.forms import LoginForm


def login_user(request):
    """Авторизация пользователя"""
    context = {
        'title': 'Авторизация',
        'login_form': LoginForm(),
    }
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('index')
            else:
                context = {
                    'login_form': login_form,
                    'attention': f"Неправильное имя пользователя или пароль!",
                }

    return render(request, 'auth/login.html', context)


def register_user(request):
    """Регистрация пользователя"""
    context = {'title': 'Регистрация'}
    return render(request, 'auth/register.html', context)


def logout_user(request):
    """Выйти"""
    logout(request)
    return redirect('index')
