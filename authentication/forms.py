from django import forms


class LoginForm(forms.Form):
    """Форма авторизации"""
    username = forms.CharField(label='Имя пользователя')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')
