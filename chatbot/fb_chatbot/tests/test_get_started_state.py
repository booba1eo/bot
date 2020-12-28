# Copyright (c) 2019 Celadon Development LLC, All rights reserved.
# Author Hleb Serafimovich <hleb.serafimovich@celadon.ae>

# pylint: disable=W0613,W0621,W0221

from unittest import mock

from django.test import TestCase

from requests.exceptions import HTTPError

from fb_chatbot import msg
from fb_chatbot.bot import Bot
from fb_chatbot.bot_storage import StateStorage
from fb_chatbot.fb_api import post_message
from fb_chatbot.models import Chain
from fb_chatbot.tests.factories import ChainFactory
from fb_chatbot.tests.utils import mock_get_user_info

from fb_chatbot.states.get_started import GetStartedState


class GetStartedStateTestCase(TestCase):
    def setUp(self):
        self.facility = ChainFactory()
        self.psid = 2455510957794561
        self.bot = Bot(self.psid)
        self.user_info = mock_get_user_info(self.psid)
        self.facility_info = Chain.objects.get(name='BSUIR BURGERS')

    @mock.patch('fb_chatbot.states.get_started.get_user_info', side_effect=mock_get_user_info)
    def test_valid_input(self, mock_get_user_info):
        response = self.bot.process_message(msg.GET_STARTED)
        response_equal = GetStartedState.get_start_msg(self.user_info, self.facility_info)
        self.assertEqual(response, response_equal)
        self.assertIsInstance(self.bot.state, GetStartedState)
        self.assertEqual(self.bot.state.context, StateStorage.context_default)
        response = self.bot.process_message(msg.ORDER_TO_GO)
        response_equal = GetStartedState.get_order_to_go_msg()
        self.assertEqual(response, response_equal)
        self.assertIsInstance(self.bot.state, GetStartedState)
        self.assertEqual(self.bot.state.context, StateStorage.context_default)

    @mock.patch('fb_chatbot.states.get_started.get_user_info', side_effect=mock_get_user_info)
    def test_invalid_input(self, mock_get_user_info):
        self.bot.process_message(msg.GET_STARTED)
        response = self.bot.process_message('invalid')
        response_equal = GetStartedState.get_unkown_msg()
        self.assertEqual(response, response_equal)
        self.assertIsInstance(self.bot.state, GetStartedState)
        self.assertEqual(self.bot.state.context, StateStorage.context_default)
        response = self.bot.process_message(msg.HOME)
        response_equal = GetStartedState.get_start_msg(self.user_info, self.facility_info)
        self.assertEqual(response, response_equal)
        self.assertIsInstance(self.bot.state, GetStartedState)
        self.assertEqual(self.bot.state.context, StateStorage.context_default)

    def test_invalid_id(self):
        self.bot = Bot('1213sadsa')
        self.assertRaises(
            HTTPError,
            post_message,
            GetStartedState.get_start_msg(self.user_info, self.facility_info))
