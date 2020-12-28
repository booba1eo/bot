# Copyright (c) 2019 Celadon Development LLC, All rights reserved.
# Author Hleb Serafimovich <hleb.serafimovich@celadon.ae>

from django import forms

from payment.models import User


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User

        fields = [
            'username',
            'password',
            'first_name',
            'last_name',
            'birthday',
            'gender',
            'email',
            'mobile_number',
        ]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'input-menu__form-input'}),
            'password': forms.PasswordInput(attrs={'class': 'input-menu__form-input'}),
            'first_name': forms.TextInput(attrs={'class': 'input-menu__form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'input-menu__form-input'}),
            'mobile_number': forms.NumberInput(attrs={'class': 'input-menu__form-input'}),
            'birthday': forms.DateInput(attrs={'type': 'date', 'class': 'input-menu__form-input'}),
            'email': forms.EmailInput(attrs={'class': 'input-menu__form-input'}),
            'gender': forms.Select(attrs={'class': 'input-menu__form-select'}),
        }


class LoginForm(forms.ModelForm):
    class Meta:
        model = User

        fields = [
            'username',
            'password',
        ]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'input-menu__form-input'}),
            'password': forms.PasswordInput(attrs={'class': 'input-menu__form-input'}),
        }
