from django import forms
from .models import *


class SignUpForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['position'].empty_label = 'Выберите должность'

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'full_name', 'position']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'input'}),
            'password1': forms.PasswordInput(attrs={'class': 'input'}),
            'password2': forms.PasswordInput(attrs={'class': 'input'}),
            'full_name': forms.TextInput(attrs={'class': 'input'}),
            'position': forms.Select(attrs={'class': 'input'})
        }
