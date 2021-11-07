from itertools import islice

from django.db.models import Q
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect

from regapp.forms import *
from .models import *

from passlib.hash import pbkdf2_sha256


def index(request, catId=0):
    context = {'title': 'Главная', 'count': request.session.get('count', False)}
    if 'username' in request.session:
        context['username'] = request.session['username']
        context['categories'] = Category.objects.all()
        context['catId'] = catId
        searchTxt = request.GET.get('search', False)
        if searchTxt:
            context['equipments'] = Equipment.objects.filter(Q(name__icontains=searchTxt) |
                                                             Q(slug__icontains=searchTxt) |
                                                             Q(description__icontains=searchTxt))
        else:
            context['equipments'] = Equipment.objects.all() if catId == 0 else (
                Equipment.objects.filter(category=Category.objects.get(id=catId))
            )
        return render(request, 'regapp/main.html', context=context)
    return render(request, 'regapp/index.html', context=context)


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
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            try:
                user = User.objects.get(username=cd['username'])
                if pbkdf2_sha256.verify(cd['password1'], user.password1):
                    request.session.set_expiry(0)
                    request.session['username'] = cd['username']
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
    request.session.clear()
    return redirect('index')


def equipment(request, slug=1):
    count = int(request.POST.get('count', False))
    if count:
        request.session['count'] = request.session['count'] + count if 'count' in request.session else count
        if 'equipments' in request.session:
            if slug in request.session['equipments']:
                request.session['equipments'][slug] += count
            else:
                request.session['equipments'][slug] = count
        else:
            request.session['equipments'] = {slug: count}
    context = {'title': f'Оборудование · {slug}',
               'username': request.session['username'],
               'count': request.session.get('count', False),
               'e': Equipment.objects.get(slug=slug)}
    return render(request, 'regapp/equipment.html', context=context)


def myApp(request, appId):
    context = {'title': f'Заявка №{appId}',
               'username': request.session['username'],
               'user': User.objects.get(username=request.session['username']),
               'count': request.session.get('count', False),
               'app': Application.objects.get(id=appId),
               'appEqs': ApplicationEquipment.objects.filter(application__id=appId)}
    return render(request, 'regapp/myApp.html', context=context)


def myApplications(request):
    apps = Application.objects.filter(user__username=request.session['username']
                                      ) if 'username' in request.session else False
    context = {'title': 'Мои заявки',
               'username': request.session['username'],
               'count': request.session.get('count', False),
               'apps': apps}
    return render(request, 'regapp/myApplications.html', context=context)


def regApp(request):
    equipments = []
    submit = False
    if 'equipments' in request.session:
        # if 'equipmentsBackup' not in request.session:
        #     request.session['equipmentsBackup'] = request.session['equipments']
        if request.method == 'POST':
            request.session['equipments'] = {}
            default = False
            for k, v in request.POST.items():
                if 'equipment' in k:
                    idx = int(k.split('_')[1])
                    if len(v) > 0 and f'x_{idx}' not in request.POST:
                        slug = v if Equipment.objects.filter(slug=v).count() > 0 else Equipment.objects.get(
                            name=v).slug
                        count = int(request.POST[f'count_{idx}']) if len(request.POST[f'count_{idx}']) > 0 else 0
                        request.session['equipments'][slug] = count if slug not in request.session['equipments'] else (
                                request.session['equipments'][slug] + count)
                    elif len(v) == 0:
                        default = True
                        if f'x_{idx}' in request.POST:
                            default = False
            if 'add' in request.POST or default:
                request.session['equipments'][''] = ''
            elif 'submit' in request.POST:
                submit = True
        for k, v in request.session['equipments'].items():
            equipments.append({'equipment': Equipment.objects.get(
                slug=k) if Equipment.objects.filter(slug=k).exists() else '',
                               'count': v,
                               'index': len(equipments)})
    context = {'title': 'Регистрация заявки',
               'username': request.session['username'],
               'count': request.session.get('count', False),
               'institution': Institution.objects.all(),
               'equipments': equipments,
               'all_equipments': Equipment.objects.all(),
               'categories': Category.objects.all()}
    if submit:
        return render(request, 'regapp/myApp.html', context=context)
    else:
        return render(request, 'regapp/regApp.html', context=context)


def pageNotFound(request, exception):
    return HttpResponseNotFound('Страница не найдена!')
