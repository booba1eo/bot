# Copyright (c) 2019 Celadon Development LLC, All rights reserved.
# Author Hleb Serafimovich <hleb.serafimovich@celadon.ae>

# pylint: disable=R0901

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

from payment.forms import RegistrationForm, LoginForm
from rest_framework import status
from requests.models import Response
from django.core.exceptions import ValidationError


class Registration(generic.CreateView):
    form_class = RegistrationForm
    template_name = 'payment/registration.html'
    success_url = reverse_lazy('payment:home_page')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        print('valid', form.is_valid())
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()
            return redirect(self.success_url)


class Login(generic.View):
    form_class = LoginForm
    template_name = 'payment/login.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            home_url = reverse_lazy('payment:home_page')
            return redirect(home_url)

        context = {
            'form': form,
            'login_error': 'User not found'
        }
        return render(request, self.template_name, context)


class HomePage(generic.View):
    template_name = 'payment/home_page.html'

    def get(self, request, *args, **kwargs):
        if request.session.get('_auth_user_id', False):
            return render(request, self.template_name)

        login_url = reverse_lazy('payment:login')
        return redirect(login_url)


def loggout(request):
    logout(request)
    login_url = reverse_lazy('payment:login')
    return redirect(login_url)
