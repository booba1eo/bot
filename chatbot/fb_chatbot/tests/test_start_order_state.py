# Copyright (c) 2019 Celadon Development LLC, All rights reserved.
# Author Hleb Serafimovich <hleb.serafimovich@celadon.ae>

# pylint: disable=W0613,W0621,W0221

from unittest import mock

from django.test import TestCase

from fb_chatbot import msg
from fb_chatbot.bot import Bot
from fb_chatbot.bot_storage import StateStorage
from fb_chatbot.models import Facility, Menu, Item, Order
from fb_chatbot.tests.factories import ItemFactory
from fb_chatbot.tests.utils import mock_get_user_info

from fb_chatbot import states


class StartOrderStateTestCase(TestCase):
    @mock.patch('fb_chatbot.states.get_started.get_user_info', side_effect=mock_get_user_info)
    def setUp(self, mock_get_user_info):
        self.item = ItemFactory()
        self.facility = Facility.objects.first()
        self.menu = Menu.objects.first()
        self.psid = 2455510957794561
        self.bot = Bot(self.psid)
        self.bot.process_message(msg.GET_STARTED)
        self.bot.process_message(msg.ORDER_TO_GO)
        self.bot.process_message({'lat': 53.903541, 'long': 27.551523})

    def test_valid_select_facility(self):
        menu_types = Menu.objects.filter(facility__id=self.facility.id)
        response = self.bot.process_message(f'{msg.SELECT_FACILITY}:{self.facility.id}')
        response_equal = states.StartOrderState.get_main_menu_msg(menu_types)
        self.assertEqual(response, response_equal)
        self.assertIsInstance(self.bot.state, states.StartOrderState)
        self.assertEqual(self.bot.state.context['facility_id'], str(self.facility.id))

    def test_invalid_select_facility(self):
        response = self.bot.process_message('invalid')
        response_equal = states.StartOrderState.get_unkown_msg()
        self.assertEqual(response, response_equal)
        self.assertIsInstance(self.bot.state, states.StartOrderState)
        self.assertEqual(self.bot.state.context, StateStorage.context_default)

    def test_valid_select_menu(self):
        items = Item.objects.all()
        self.bot.process_message(f'{msg.SELECT_FACILITY}:{self.facility.id}')
        response = self.bot.process_message(f'{self.menu.category},top')
        response_equal = states.StartOrderState.get_items_msg(items)
        self.assertEqual(response, response_equal)
        self.assertIsInstance(self.bot.state, states.StartOrderState)
        self.assertEqual(self.bot.state.context['type_of_menu'], self.menu.category)
        self.assertEqual(self.bot.state.context['type_of_button'], 'top')

    @mock.patch('fb_chatbot.states.get_started.get_user_info', side_effect=mock_get_user_info)
    def test_invalid_select_menu(self, mock_get_user_info):
        self.bot.process_message(f'{msg.SELECT_FACILITY}:{self.facility.id}')
        response = self.bot.process_message(f'{msg.USER_TAG}:invalid')
        response_equal = states.StartOrderState.get_unkown_msg()
        self.assertEqual(response, response_equal)
        self.assertIsInstance(self.bot.state, states.StartOrderState)
        self.bot.process_message(f'{msg.HOME}')
        self.assertIsInstance(self.bot.state, states.GetStartedState)
        self.assertEqual(self.bot.state.context, StateStorage.context_default)

    def test_valid_select_item(self):
        self.bot.process_message(f'{msg.SELECT_FACILITY}:{self.facility.id}')
        self.bot.process_message(f'{self.menu.category},top')
        response = self.bot.process_message(f'{msg.SELECT_ITEM}:{self.item.id}')
        response_equal = states.StartOrderState.get_select_item_msg(self.item, 1)
        order = Order.objects.first()
        self.assertEqual(response, response_equal)
        self.assertIsInstance(self.bot.state, states.StartOrderState)
        self.assertEqual(self.bot.state.context['item_id'], self.item.id)
        self.assertEqual(self.bot.state.context['order_id'], order.id)

    def test_invalid_select_item(self):
        self.bot.process_message(f'{msg.SELECT_FACILITY}:{self.facility.id}')
        self.bot.process_message(f'{self.menu.category},top')
        response = self.bot.process_message(f'{msg.USER_TAG}:invalid')
        response_equal = states.StartOrderState.get_unkown_msg()
        self.assertEqual(response, response_equal)
        self.assertIsInstance(self.bot.state, states.StartOrderState)
        self.assertEqual(self.bot.state.context['item_id'], None)
        self.assertEqual(self.bot.state.context['order_id'], None)

    def test_back_button(self):
        menu_types = Menu.objects.filter(facility__id=self.facility.id)
        self.bot.process_message(f'{msg.SELECT_FACILITY}:{self.facility.id}')
        self.bot.process_message(f'{self.menu.category},top')
        response = self.bot.process_message(f'{msg.BACK}:{msg.MAIN_MENU}')
        response_equal = states.StartOrderState.get_main_menu_msg(menu_types)
        self.assertEqual(response, response_equal)
        self.assertIsInstance(self.bot.state, states.StartOrderState)
