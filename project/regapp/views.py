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


# !!!!!!!!!!!!!!!!
def signOut(request):
    # del request.session['username']
    for k in request.session.keys():
        del request.session[k]

    return redirect('index')


def equipment(request, slug=1):
    count = int(request.POST.get('count', False))
    if count:
        request.session['count'] = request.session['count'] + count if 'count' in request.session else count
        request.session['slugs'] = request.session['slugs'] + ' ' + slug if 'slug' in request.session else slug
        request.session['counts'] = request.session['counts'] + ' ' + str(count) if 'counts' in request.session else str(count)
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
    apps = Application.objects.filter(user__username=request.session['username']) if 'username' in request.session else False
    context = {'title': 'Мои заявки',
               'username': request.session['username'],
               'count': request.session.get('count', False),
               'apps': apps}
    return render(request, 'regapp/myApplications.html', context=context)


def regApp(request):

    print('\n\n')
    print(request.session['counts'])
    print('\n\n')

    equipments = []
    if 'slugs' in request.session:
        slugs = request.session['slugs'].split(' ')
        counts = [int(c) for c in request.session['counts'].split(' ')]
        scDict = {}
        for i, v in enumerate(slugs):
            scDict[v] = scDict[v] + counts[i] if v in scDict else counts[i]
        for k, v in scDict.items():
            equipments.append({'equipment': Equipment.objects.get(slug=k), 'count': v})
    context = {'title': 'Регистрация заявки',
               'username': request.session['username'],
               'count': request.session['count'],
               'institution': Institution.objects.all(),
               'equipments': equipments,
               'all_equipments': Equipment.objects.all(),
               'categories': Category.objects.all()}
    return render(request, 'regapp/regApp.html', context=context)


def pageNotFound(request, exception):
    return HttpResponseNotFound('Страница не найдена!')
