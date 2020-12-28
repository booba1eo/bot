# Copyright (c) 2019 Celadon Development LLC, All rights reserved.
# Author Hleb Serafimovich <hleb.serafimovich@celadon.ae>

from django.test import TestCase
from django.urls import reverse

from payment.forms import LoginForm
from payment.models import User


class RegistrationTestCase(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'boobaleo',
            'password': 'password'
        }
        self.login_url = reverse('payment:login')
        User.objects.create_user(**self.credentials)

    def test_valid_login(self):
        response = self.client.post(self.login_url, self.credentials, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)

    def test_invalid_login(self):
        invalid_credentials = {
            'username': 'bob',
            'password': '123pass'
        }
        response = self.client.post(self.login_url, invalid_credentials, follow=True)
        self.assertFalse(response.context['user'].is_authenticated)
