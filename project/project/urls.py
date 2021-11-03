from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from project import settings
from regapp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('<int:catId>/', index, name='index'),
    path('signUp/', signUp, name='signUp'),
    path('signIn/', signIn, name='signIn'),
    path('signOut/', signOut, name='signOut'),
    path('regApp/', regApp, name='regApp'),
    path('equipment/', equipment, name='equipment'),
    path('equipment/<slug:slug>', equipment, name='equipment'),
    path('myApp/<int:appId>/', myApp, name='myApp'),
    path('myApplications/', myApplications, name='myApplications'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = pageNotFound
