from django.db import models
from django.db.models import CASCADE
from phonenumber_field.modelfields import PhoneNumberField


class Position(models.Model):
    name = models.CharField(max_length=100, verbose_name='Должность')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'


class User(models.Model):
    username = models.CharField(max_length=50, unique=True, db_index=True, verbose_name='Логин')
    password1 = models.CharField(max_length=100, verbose_name='Пароль')
    password2 = models.CharField(max_length=100, verbose_name='Подтверждение пароля')
    full_name = models.CharField(max_length=100, verbose_name='ФИО')
    position = models.ForeignKey('Position', on_delete=CASCADE, verbose_name='Должность')

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Founder(models.Model):
    name = models.CharField(max_length=255, verbose_name='Учредитель')
    address = models.CharField(max_length=255, verbose_name='Адрес')
    phone_number = PhoneNumberField(verbose_name='Номер телефона')
    email = models.EmailField(verbose_name='Email')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Учредитель'
        verbose_name_plural = 'Учредители'


class Institution(models.Model):
    name = models.CharField(max_length=255, verbose_name='Образовательное учреждение')
    short_name = models.CharField(max_length=50, verbose_name='ОУ сокр.')
    founder = models.ForeignKey('Founder', on_delete=CASCADE, verbose_name='Учредитель')

    def __str__(self):
        return self.short_name

    class Meta:
        verbose_name = 'Образовательное учреждение'
        verbose_name_plural = 'Образовательные учреждения'


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Категория оборудования')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория оборудования'
        verbose_name_plural = 'Категории оборудования'


class Equipment(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True, verbose_name='Оборудование')
    slug = models.SlugField(unique=True, db_index=True, verbose_name='Артикул')
    price = models.CharField(max_length=50, default='предоставляется по запросу', verbose_name='Цена')
    description = models.TextField(blank=True, verbose_name='Описание')
    image = models.ImageField(upload_to='images/%Y/%m/%d/', verbose_name='Изображение')
    category = models.ForeignKey('Category', on_delete=CASCADE, verbose_name='Категория оборудования')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Оборудование'
        verbose_name_plural = 'Оборудование'


class Application(models.Model):
    date = models.DateField(auto_now_add=True, verbose_name='Дата')
    educational_institution = models.ForeignKey('Institution', on_delete=CASCADE,
                                                verbose_name='Образовательное учреждение')
    user = models.ForeignKey('User', on_delete=CASCADE, verbose_name='Пользователь')

    def __str__(self):
        return self.date

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'


class ApplicationEquipment(models.Model):
    count = models.PositiveSmallIntegerField(default=1, verbose_name='Кол-во')
    application = models.ForeignKey('Application', on_delete=CASCADE, verbose_name='Заявка')
    equipment = models.ForeignKey('Equipment', on_delete=CASCADE, verbose_name='Оборудование')

    def __str__(self):
        return self.count

    class Meta:
        verbose_name = 'Оборудование заявок'
        verbose_name_plural = 'Оборудование заявок'
