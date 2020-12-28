# Copyright (c) 2019 Celadon Development LLC, All rights reserved.
# Author Hleb Serafimovich <hleb.serafimovich@celadon.ae>

import datetime

from django.test import TestCase

from payment.forms import RegistrationForm


class RegistrationTestCase(TestCase):
    def test_valid_input_form(self):
        form_data = {
            'username': 'boobaleo',
            'password': 'passSuperPass11',
            'first_name': 'Hleb',
            'last_name': 'Serafim',
            'email': 'hleb.serafimovich@celadon.ae',
            'mobile_number': 375336252768,
            'birthday': '1999-08-05',
            'gender': 'male',
        }
        form = RegistrationForm(data=form_data)
        user = form.save()
        self.assertTrue(form.is_valid())
        self.assertEqual(user.first_name, 'Hleb')
        self.assertEqual(user.last_name, 'Serafim')
        self.assertEqual(user.email, 'hleb.serafimovich@celadon.ae')
        self.assertEqual(user.mobile_number, 375336252768)
        self.assertEqual(user.birthday, datetime.date(1999, 8, 5))
        self.assertEqual(user.gender, 'male')

    def test_invalid_input_form(self):
        form_data = {
            'username': 123,
            'password': '',
            'first_name': 123,
            'last_name': 123,
            'email': 123,
            'mobile_number': 'invalid',
            'birthday': 'ivalid',
            'gender': 'invalid',
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_blank_input_form(self):
        form_data = {}
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'first_name': ['This field is required.'],
            'last_name': ['This field is required.'],
            'email': ['This field is required.'],
            'username': ['This field is required.'],
            'password': ['This field is required.'],
            'birthday': ['This field is required.'],
            'gender': ['This field is required.'],
            'mobile_number': ['This field is required.'],
        })
