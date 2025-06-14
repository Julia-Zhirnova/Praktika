from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .forms import RegistrationForm
from django.contrib.auth.decorators import user_passes_test

from django.contrib.auth.decorators import login_required
from .models import Praktiki, PeriodyPraktiki, Specialnosti, SpecialnostiGruppy, UchebnyjPlan, ProfessionalnyeModuli, Tip


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

# для вывода данных
from django.shortcuts import get_object_or_404
from .models import Praktiki, Zadaniya, UchebnyjPlan
from .models import Praktiki, PeriodyPraktiki, Specialnosti, SpecialnostiGruppy, UchebnyjPlan, ProfessionalnyeModuli, Tip, Zadaniya

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import (Praktiki, PeriodyPraktiki, Specialnosti, 
                    SpecialnostiGruppy, UchebnyjPlan, 
                    ProfessionalnyeModuli, Zadaniya, RukovoditeliPraktik)

@login_required
def user_panel(request):
    # Получаем текущего пользователя
    user = request.user

    # Получаем все практики, связанные с пользователем через related_name
    praktiki = Praktiki.objects.filter(rukovoditeli__rukovoditel_nomer=user)

    # Собираем данные для каждой практики
    data = []
    for praktika in praktiki:
        period = praktika.period_nomer
        tip = period.tip_kod
        specialnost = praktika.specialnost_kod
        gruppy = SpecialnostiGruppy.objects.filter(specialnosti_kod=specialnost)
        modul = praktika.modul_nomer  # Это объект модели ProfessionalnyeModuli
        mdks = ProfessionalnyeModuli.objects.filter(modul_nomer=modul)

        # Форматируем даты
        data_nachala = period.data_nachala.strftime('%d.%m.%Y')
        data_okonchaniya = period.data_okonchaniya.strftime('%d.%m.%Y')

        # Генерируем название практики
        try:
            # Извлекаем номер модуля
            
            modul_nomer = modul.naimenovanie_modulya.split()[0].split('.')[1]
        except (AttributeError, IndexError):
            modul_nomer = "Н/Д"  # Если номер модуля не найден, используем значение по умолчанию

        # Получаем первую группу из QuerySet
        gruppa = gruppy.first()
        praktika_nazvanie = f"Группа_{gruppa.nazvanie_gruppy if gruppa else 'Н/Д'}_{period.god}_Задание_ПП{modul_nomer}"

        # Добавляем данные в список
        data.append({
            'nomer_praktiki': praktika.nomer_praktiki,
            'praktika_nazvanie': praktika_nazvanie,
            'god': period.god,
            'naimenovanie_tipa': tip.naimenovanie_tipa if tip else None,
            'kod_specialnosti': specialnost.kod_specialnosti,
            'nazvanie_specialnosti': specialnost.nazvanie_specialnosti,
            'nazvanie_gruppy': ', '.join([gruppa.nazvanie_gruppy for gruppa in gruppy]) if gruppy.exists() else 'Н/Д',
            'naimenovanie_modulya': modul.naimenovanie_modulya if modul and modul.naimenovanie_modulya else 'Н/Д',
            'naimenovanie_mdk': ', '.join([mdk.naimenovanie_mdk for mdk in mdks]) if mdks.exists() else 'Н/Д',
            'obem_v_chasah': period.obem_v_chasah,
            'data_nachala': data_nachala,
            'data_okonchaniya': data_okonchaniya,
            'praktika_id': praktika.nomer_praktiki,  # Для ссылки на детальную страницу
        })

    # Передаем данные в шаблон
    return render(request, 'main/user_panel.html', {'data': data})

def praktika_detail(request, pk):
    # Получаем практику по ее номеру
    praktika = get_object_or_404(Praktiki, nomer_praktiki=pk)
    # Проверяем, что modul_nomer существует
    if not praktika.modul_nomer:
        return render(request, 'main/praktika_detail.html', {
            'error': 'Модуль для данной практики не найден.'
        })
    # Получаем связанные данные
    period = praktika.period_nomer
    uchebnyj_plan = praktika.modul_nomer  # Это объект модели UchebnyjPlan
    mdks = ProfessionalnyeModuli.objects.filter(modul_nomer=uchebnyj_plan.nomer_modulya)
    zadaniya = Zadaniya.objects.filter(praktika_nomer=praktika)
    # Формируем название практики
    gruppa = SpecialnostiGruppy.objects.filter(specialnosti_kod=praktika.specialnost_kod).first()
    praktika_nazvanie = f"Группа_{gruppa.nazvanie_gruppy if gruppa else 'Н/Д'}_{period.god}_Задание_ПП{uchebnyj_plan.nomer_modulya.split('_')[-1]}"
    # Собираем данные для таблицы
    table_data = []
    for zadanie in zadaniya:
        kompetencii = uchebnyj_plan.kompetencii or 'Н/Д'
        table_data.append({
            'nazvanie_temy': zadanie.nazvanie_temy,
            'vidy_rabot': zadanie.vidy_rabot,
            'kompetencii': kompetencii,
            'kolichestvo_chasov_na_odnu_rabotu': zadanie.kolichestvo_chasov_na_odnu_rabotu,
        })
    return render(request, 'main/praktika_detail.html', {
        'praktika': praktika,
        'praktika_nazvanie': praktika_nazvanie,
        'table_data': table_data,
    })