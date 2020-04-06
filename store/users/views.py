from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from users.forms import UserRegistrationForm, UserLoginForm


def register_view(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Создаем новый объект User, но не сохраняем его
            new_user = user_form.save(commit=False)
            # Проверяем пароль
            new_user.set_password(user_form.cleaned_data['password'])
            # Сохраняем объект
            new_user.save()
            context = {
                'new_user': new_user
            }

            return render(request, 'users/register_done.html', context)
    else:
        user_form = UserRegistrationForm()
    context = {
        'user_form': user_form
    }

    return render(request, 'users/register.html', context)


def login_view(request):
    if request.method == 'POST':
        user_form = UserLoginForm(request.POST)
        if user_form.is_valid():
            user = user_form.login(request)
            if user:
                login(request, user)
                return redirect('main:shop')
    else:
        user_form = UserLoginForm()
    context = {
        'user_form': user_form
    }

    return render(request, 'users/login.html', context)


@login_required
def logout_view(request):
    logout(request)
    return render(request, 'users/logged_out.html')
