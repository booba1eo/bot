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

from fb_chatbot import states


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

    def test_valid_add_item_to_order(self):
        facility_info = models.Chain.objects.get(name='BSUIR BURGERS')
        item_order_records = models.ItemOrder.objects.filter(order=self.bot.state.context['order_id'])
        order = models.Order.objects.first()
        response = self.bot.process_message(msg.ADD_ITEM_TO_ORDER)
        response_equal = states.CheckOrderMenuState.get_check_order_menu_msg(
            facility_info,
            item_order_records)
        self.assertEqual(response, response_equal)
        self.assertIsInstance(self.bot.state, states.SelectItemMenuState)
        self.assertEqual(self.bot.state.context['type_of_button'], 'top')
        self.assertEqual(self.bot.state.context['item_id'], self.item.id)
        self.assertEqual(self.bot.state.context['order_id'], order.id)

    def test_valid_change_item_count(self):
        response = self.bot.process_message(msg.CHANGE_QUANTITY_ITEM)
        response_equal = states.SelectItemMenuState.get_change_quantity_msg()
        self.assertEqual(response, response_equal)
        self.assertIsInstance(self.bot.state, states.SelectItemMenuState)
        response = self.bot.process_message(f'{msg.QUANTITY_BUTTON}:3')
        self.assertEqual(self.bot.state.context['item_count'], '3')

    @mock.patch('fb_chatbot.states.get_started.get_user_info', side_effect=mock_get_user_info)
    def test_invalid_change_item_count(self, mock_get_user_info):
        response = self.bot.process_message('invalid')
        response_equal = states.SelectItemMenuState.get_unkown_msg()
        self.assertEqual(response, response_equal)
        self.bot.process_message(msg.ORDER_TO_GO)
        self.assertIsInstance(self.bot.state, states.GetStartedState)
        self.assertEqual(self.bot.state.context, StateStorage.context_default)
