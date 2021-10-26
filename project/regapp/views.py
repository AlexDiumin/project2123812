from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect

from regapp.forms import *
from .models import *

from passlib.hash import pbkdf2_sha256


USERNAME = ''


def index(request, catId=0):
    context = {'title': 'Главная', 'username': USERNAME}
    if USERNAME:
        context['catId'] = catId
        context['categories'] = Category.objects.all()
        context['equipments'] = Equipment.objects.all() if catId == 0 else (
            Equipment.objects.filter(category=Category.objects.get(id=catId))
        )
        return render(request, 'regapp/main.html', context=context)
    return render(request, 'regapp/index.html', context=context)


# def main(request, catId):
#     context = {'title': 'Главная',
#                'username': USERNAME,
#                'categories': Category.objects.all(),
#                'catId': catId}
#     if catId > 0:
#         context['equipments'] = Equipment.objects.filter(category=Category.objects.get(id=catId))
#     else:
#         context['equipments'] = Equipment.objects.all()
#     return render(request, 'regapp/main.html', context=context)


def signUp(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('signIn')
    else:
        form = SignUpForm()
    context = {'title': 'Регистрация', 'form': form}
    return render(request, 'regapp/signUp.html', context=context)


def signIn(request):
    global USERNAME
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            try:
                user = User.objects.get(username=cd['username'])
                if pbkdf2_sha256.verify(cd['password1'], user.password1):
                    USERNAME = cd['username']
                    return redirect('index')
                else:
                    form.add_error(None, 'Неверный пароль.')
            except:
                form.add_error(None, 'Пользователь с указанным логином не найден.')
    else:
        form = SignInForm()
    context = {'title': 'Авторизация', 'form': form}
    return render(request, 'regapp/signIn.html', context=context)


def signOut(request):
    global USERNAME
    USERNAME = ''
    return redirect('index')


def equipment(request):
    context = {'title': 'Наименование оборудования'}
    return render(request, 'regapp/equipment.html', context=context)


def myApp(request):
    context = {'title': 'Заявка №15'}
    return render(request, 'regapp/myApp.html', context=context)


def myApplications(request):
    context = {'title': 'Мои заявки', 'username': USERNAME}
    return render(request, 'regapp/myApplications.html', context=context)


def regApp(request):
    context = {'title': 'Регистрация заявки'}
    return render(request, 'regapp/regApp.html', context=context)


def pageNotFound(request, exception):
    return HttpResponseNotFound('Страница не найдена!')
