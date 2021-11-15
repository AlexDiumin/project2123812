from django.contrib.auth import logout
from django.db.models import Q
from django.http import HttpResponseNotFound
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
            context['searchTxt'] = searchTxt
            context['equipments'] = Equipment.objects.filter(Q(name__icontains=searchTxt) |
                                                             Q(name__icontains=searchTxt.lower()) |
                                                             Q(name__icontains=searchTxt.upper()) |
                                                             Q(slug__icontains=searchTxt) |
                                                             Q(slug__icontains=searchTxt.lower()) |
                                                             Q(slug__icontains=searchTxt.upper()) |
                                                             Q(description__icontains=searchTxt) |
                                                             Q(description__icontains=searchTxt.lower()) |
                                                             Q(description__icontains=searchTxt.upper()))
        if 'equipments' not in context or context['equipments'].count() == 0:
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
    logout(request)
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
    request.session['selected_institution'] = False
    if 'equipments' not in request.session:
        request.session['equipments'] = {}
    if request.method == 'POST':
        if 'institution' in request.POST:
            request.session['selected_institution'] = request.POST['institution']
        default = False
        request.session['equipments'] = {}
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
        if 'submit' in request.POST:
            submit = True
    for k, v in request.session['equipments'].items():
        equipments.append({'equipment': Equipment.objects.get(
            slug=k) if Equipment.objects.filter(slug=k).exists() else '',
                           'count': v,
                           'index': len(equipments)})
    if submit:
        application = Application.objects.create(
            educational_institution=Institution.objects.get(id=request.POST['institution']),
            user=User.objects.get(username=request.session['username']))
        for eq in equipments:
            if eq['equipment'] != '':
                ApplicationEquipment.objects.create(count=eq['count'],
                                                    application=application,
                                                    equipment=eq['equipment'])
        context = {'title': f'Заявка №{application.id}',
                   'username': request.session['username'],
                   'user': User.objects.get(username=request.session['username']),
                   'count': request.session.get('count', False),
                   'app': application,
                   'appEqs': ApplicationEquipment.objects.filter(application__id=application.id)}
        if 'count' in request.session:
            del request.session['count']
        if 'equipments' in request.session:
            del request.session['equipments']
        if 'selected_institution' in request.session:
            del request.session['selected_institution']
        return render(request, 'regapp/myApp.html', context=context)
    else:
        context = {'title': 'Регистрация заявки',
                   'username': request.session['username'],
                   'count': request.session.get('count', False),
                   'institutions': Institution.objects.all(),
                   'selected_institution': Institution.objects.get(
                       id=request.session['selected_institution']) if request.session['selected_institution'] else False,
                   'equipments': equipments,
                   'all_equipments': Equipment.objects.all(),
                   'categories': Category.objects.all()}
        return render(request, 'regapp/regApp.html', context=context)


def pageNotFound():
    return HttpResponseNotFound('Страница не найдена!')
