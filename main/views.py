from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .forms import RegistrationForm
from django.contrib.auth.decorators import user_passes_test

def index(request):
    return render(request, 'main/index.html')

def register(request):
    return render(request, 'main/register.html')

def login_view(request):
    return render(request, 'main/login.html')

def admin_panel(request):
    return render(request, 'main/admin_panel.html')

def user_panel(request):
    return render(request, 'main/user_panel.html')

def search(request):
    query = request.GET.get('q', '')
    results = []  # Здесь можно добавить логику поиска (например, из базы данных)
    return render(request, 'main/search_results.html', {'query': query, 'results': results})

# Аутентификация
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data['email']  # Используем email как логин
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect('login')  # Перенаправляем на страницу входа
    else:
        form = RegistrationForm()
    return render(request, 'main/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        # Аутентификация пользователя
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')  # Перенаправляем на главную страницу
        else:
            return render(request, 'main/login.html', {'error': 'Неверный логин или пароль'})
    return render(request, 'main/login.html')

def logout_view(request):
    logout(request)
    return redirect('index')

# админ
def admin_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        # Аутентификация пользователя
        user = authenticate(request, username=email, password=password)
        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('/admin/')  # Перенаправляем на админ-панель
        else:
            return render(request, 'main/admin_login.html', {'error': 'Неверный логин или пароль администратора'})

    return render(request, 'main/admin_login.html')
