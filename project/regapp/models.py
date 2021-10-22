from django.conf import settings
from django.db import models
from django.db.models import CASCADE
from phonenumber_field.modelfields import PhoneNumberField


# Учредитель
class Founder(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone_number = PhoneNumberField()
    email = models.EmailField()


# Образовательное учреждение
class Institution(models.Model):
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=50)
    founder = models.ForeignKey('Founder', on_delete=CASCADE)


# Категория оборудования
class Category(models.Model):
    name = models.CharField(max_length=255)


# Оборудование
class Equipment(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, db_index=True)  # артикул
    price = models.CharField(max_length=50, default='предоставляется по запросу')
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/%Y/%m/%d/')
    category = models.ForeignKey('Category', on_delete=CASCADE)


# Заявка
class Application(models.Model):
    date = models.DateField(auto_now_add=True)
    educational_institution = models.ForeignKey('Institution', on_delete=CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)


# Заявка + Оборудование
class ApplicationEquipment(models.Model):
    count = models.PositiveSmallIntegerField(default=1)
    application = models.ForeignKey('Application', on_delete=CASCADE)
    equipment = models.ForeignKey('Equipment', on_delete=CASCADE)

