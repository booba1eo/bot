# Copyright (c) 2019 Celadon Development LLC, All rights reserved.
# Author Hleb Serafimovich <hleb.serafimovich@celadon.ae>

# pylint: disable=W0613,W0621,W0221

from unittest import mock

from django.test import TestCase

from fb_chatbot import msg
from fb_chatbot.bot import Bot
from fb_chatbot.bot_storage import StateStorage
from fb_chatbot.models import Facility, Chain
from fb_chatbot.tests.factories import FacilityFactory
from fb_chatbot.tests.utils import mock_get_user_info

from fb_chatbot.states import GetStartedState, FindFacilityState


class FindFacilityStateTestCase(TestCase):
    @mock.patch('fb_chatbot.states.get_started.get_user_info', side_effect=mock_get_user_info)
    def setUp(self, mock_get_user_info):
        FacilityFactory()
        self.facility = Facility.objects.all()
        self.psid = 2455510957794561
        self.bot = Bot(self.psid)
        self.bot.process_message(msg.GET_STARTED)
        self.bot.process_message(msg.ORDER_TO_GO)

    @mock.patch('fb_chatbot.states.get_started.get_user_info', side_effect=mock_get_user_info)
    def test_valid_send_location(self, mock_get_user_info):
        response = self.bot.process_message({'lat': 53.903541, 'long': 27.551523})
        response_equal = FindFacilityState.get_facilities_msg(self.facility)
        self.assertEqual(response, response_equal)
        self.assertIsInstance(self.bot.state, FindFacilityState)
        self.assertEqual(self.bot.state.context, StateStorage.context_default)

    @mock.patch('fb_chatbot.states.get_started.get_user_info', side_effect=mock_get_user_info)
    def test_invalid_send_location(self, mock_get_user_info):
        facility_info = Chain.objects.get(name='BSUIR BURGERS')
        response = self.bot.process_message({'lat': 43.903541, 'long': 57.551523})
        response_equal = FindFacilityState.get_no_facility_nearby_msg(facility_info)
        self.assertEqual(response, response_equal)
        self.bot.process_message(msg.ORDER_TO_GO)
        self.assertIsInstance(self.bot.state, GetStartedState)
        self.assertEqual(self.bot.state.context, StateStorage.context_default)

    @mock.patch('fb_chatbot.states.get_started.get_user_info', side_effect=mock_get_user_info)
    def test_valid_input_city_01(self, mock_get_user_info):
        response = self.bot.process_message(f'{msg.USER_TAG}:Minsk')
        response_equal = FindFacilityState.get_facilities_msg(self.facility)
        self.assertEqual(response, response_equal)
        self.assertIsInstance(self.bot.state, FindFacilityState)
        self.assertEqual(self.bot.state.context, StateStorage.context_default)

    @mock.patch('fb_chatbot.states.get_started.get_user_info', side_effect=mock_get_user_info)
    def test_valid_input_city_02(self, mock_get_user_info):
        response = self.bot.process_message(f'{msg.USER_TAG}: mInSk ')
        response_equal = FindFacilityState.get_facilities_msg(self.facility)
        self.assertEqual(response, response_equal)
        self.assertIsInstance(self.bot.state, FindFacilityState)
        self.assertEqual(self.bot.state.context, StateStorage.context_default)

    @mock.patch('fb_chatbot.states.get_started.get_user_info', side_effect=mock_get_user_info)
    def test_invalid_input_city(self, mock_get_user_info):
        facility_info = Chain.objects.get(name='BSUIR BURGERS')
        response = self.bot.process_message(f'{msg.USER_TAG}:invalid')
        response_equal = FindFacilityState.get_no_facility_nearby_msg(facility_info)
        self.assertEqual(response, response_equal)
        self.bot.process_message(msg.ORDER_TO_GO)
        self.assertIsInstance(self.bot.state, GetStartedState)
        self.assertEqual(self.bot.state.context, StateStorage.context_default)
