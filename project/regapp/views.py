from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render

from django.contrib import messages


def index(request):
    context = {'title': 'Главная'}
    return render(request, 'regapp/index.html', context=context)
    # return render(request, 'regapp/main.html', context=context)


def signUp(request):
    context = {'title': 'Регистрация', 'post': request.POST}
    # messages.info(request, context['post'])
    print(context['post'])
    return render(request, 'regapp/signUp.html', context=context)


def signIn(request):
    context = {'title': 'Авторизация', 'post': request.POST}
    # messages.info(request, context['post'])
    print(context['post'])
    return render(request, 'regapp/signIn.html', context=context)


def equipment(request):
    context = {'title': 'Наименование оборудования'}
    return render(request, 'regapp/equipment.html', context=context)


def myApp(request):
    context = {'title': 'Заявка №15'}
    return render(request, 'regapp/myApp.html', context=context)


def myApplications(request):
    context = {'title': 'Мои заявки'}
    return render(request, 'regapp/myApplications.html', context=context)


def regApp(request):
    context = {'title': 'Регистрация заявки'}
    return render(request, 'regapp/regApp.html', context=context)


def pageNotFound(request, exception):
    return HttpResponseNotFound('Страница не найдена!')