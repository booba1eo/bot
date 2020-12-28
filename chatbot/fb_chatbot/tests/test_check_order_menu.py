# Copyright (c) 2019 Celadon Development LLC, All rights reserved.
# Author Hleb Serafimovich <hleb.serafimovich@celadon.ae>

# pylint: disable=W0613,W0621,W0221

from unittest import mock

from django.test import TestCase

from fb_chatbot import msg
from fb_chatbot.bot import Bot
from fb_chatbot.bot_storage import StateStorage
from fb_chatbot import models
from fb_chatbot.tests.factories import ItemFactory
from fb_chatbot.tests.utils import mock_get_user_info

from fb_chatbot.states import GetStartedState, StartOrderState


class StartOrderStateTestCase(TestCase):
    @mock.patch('fb_chatbot.states.get_started.get_user_info', side_effect=mock_get_user_info)
    def setUp(self, mock_get_user_info):
        self.item = ItemFactory()
        self.facility = models.Facility.objects.first()
        self.menu = models.Menu.objects.first()
        self.psid = 2455510957794561
        self.bot = Bot(self.psid)
        self.bot.process_message(msg.GET_STARTED)
        self.bot.process_message(msg.ORDER_TO_GO)
        self.bot.process_message({'lat': 53.903541, 'long': 27.551523})
        self.bot.process_message(f'{msg.SELECT_FACILITY}:{self.facility.id}')
        self.bot.process_message(f'{self.menu.category},top')
        self.bot.process_message(f'{msg.SELECT_ITEM}:{self.item.id}')
        self.bot.process_message(msg.ADD_ITEM_TO_ORDER)

    def test_add_more_items_button(self):
        menu_types = models.Menu.objects.filter(facility__id=self.facility.id)
        order = models.Order.objects.first()
        response = self.bot.process_message(msg.ADD_MORE_ITEMS)
        response_equal = StartOrderState.get_main_menu_msg(menu_types)
        self.assertEqual(response, response_equal)
        self.assertEqual(self.bot.state.context['type_of_button'], 'top')
        self.assertEqual(self.bot.state.context['item_id'], self.item.id)
        self.assertEqual(self.bot.state.context['item_count'], 1)
        self.assertEqual(self.bot.state.context['order_id'], order.id)

    def test_remove_item_button(self):
        item_in_order = models.ItemOrder.objects.first()
        menu_types = models.Menu.objects.filter(facility__id=self.facility.id)
        response = self.bot.process_message(f'{msg.REMOVE_ITEM}:{item_in_order.id}')
        response_equal = StartOrderState.get_main_menu_msg(menu_types)
        self.assertEqual(response, response_equal)
        self.bot.process_message(f'{self.menu.category},top')
        self.assertIsInstance(self.bot.state, StartOrderState)

    @mock.patch('fb_chatbot.states.check_order_menu.get_user_info', side_effect=mock_get_user_info)
    @mock.patch('fb_chatbot.states.get_started.get_user_info', side_effect=mock_get_user_info)
    def test_cancel_order(self, mock_check_order, mock_get_started):
        user_info = mock_get_user_info(self.psid)
        facility_info = models.Chain.objects.get(name='BSUIR BURGERS')
        response = self.bot.process_message(msg.CANCEL_ORDER)
        response_equal = GetStartedState.get_start_msg(user_info, facility_info)
        self.assertEqual(response, response_equal)
        self.bot.process_message(msg.GET_STARTED)
        self.assertIsInstance(self.bot.state, GetStartedState)
        self.assertEqual(self.bot.state.context, StateStorage.context_default)
