from django import forms
from django.core.exceptions import ValidationError

from .models import *

from passlib.hash import pbkdf2_sha256


class SignUpForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['position'].empty_label = 'Выберите должность'

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'full_name', 'position']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Введите логин'}),
            'password1': forms.PasswordInput(attrs={'class': 'input', 'placeholder': 'Введите пароль'}),
            'password2': forms.PasswordInput(attrs={'class': 'input', 'placeholder': 'Введите пароль еще раз'}),
            'full_name': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Введите ФИО'}),
            'position': forms.Select(attrs={'class': 'input', 'placeholder': 'Введите должность'})
        }

    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username) >= 50:
            raise ValidationError('Длинна логина должна быть меньше 50 символов.')
        return username

    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        if len(password1) >= 50:
            raise ValidationError('Длинна пароля должна быть меньше 50 символов.')
        return pbkdf2_sha256.hash(password1)

    def clean_password2(self):
        password2 = self.cleaned_data['password2']
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            if not pbkdf2_sha256.verify(password2, password1):
                raise ValidationError('Пароли не совпадают.')
            return password1
        return pbkdf2_sha256.hash(password2)

    def clean_full_name(self):
        full_name = self.cleaned_data['full_name']
        if len(full_name) >= 100:
            raise ValidationError('Длинна ФИО должна быть меньше 100 символов.')
        return full_name


class SignInForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = ['username', 'password1']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Введите логин'}),
            'password1': forms.PasswordInput(attrs={'class': 'input', 'placeholder': 'Введите пароль'})
        }

    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username) >= 50:
            raise ValidationError('Длинна логина должна быть меньше 50 символов.')
        return username

    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        if len(password1) >= 50:
            raise ValidationError('Длинна пароля должна быть меньше 50 символов.')
        return password1
