# Copyright (c) 2019 Celadon Development LLC, All rights reserved.
# Author Hleb Serafimovich <hleb.serafimovich@celadon.ae>

from django.test import TestCase

from fb_chatbot.tests.utils import mock_get_user_info


class UtilitiesTestCase(TestCase):
    def test_mock_get_user_info(self):
        user_info = mock_get_user_info(2455510957794561)
        self.assertEqual(user_info, {'first_name': 'Aleksandr', 'id': 2455510957794561})
