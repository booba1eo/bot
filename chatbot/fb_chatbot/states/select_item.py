# Copyright (c) 2019 Celadon Development LLC, All rights reserved.
# Author Hleb Serafimovich <hleb.serafimovich@celadon.ae>

from fb_chatbot import models, msg

from fb_chatbot.states.abstract import State
from fb_chatbot.states.start_order import StartOrderState
from fb_chatbot.states.check_order_menu import CheckOrderMenuState
from fb_chatbot.states.const import (
    START_ORDER_STATE_NAME,
    GET_STARTED_STATE_NAME,
    CHECK_ORDER_MENU_STATE_NAME
)


class SelectItemMenuState(State):
    def __init__(self, context, storage, psid):
        super().__init__(context, storage, psid)
        self.context = context
        self.storage = storage
        self.psid = psid

    def process_message(self, fb_msg):
        state = None
        if fb_msg == msg.ADD_ITEM_TO_ORDER:
            state = CHECK_ORDER_MENU_STATE_NAME
            self.add_item_to_order()
            message = self.process_check_order_menu()
        elif fb_msg == msg.CHANGE_QUANTITY_ITEM:
            message = SelectItemMenuState.get_change_quantity_msg()
        elif msg.QUANTITY_BUTTON in fb_msg:
            message = self.process_quantity_button(fb_msg)
        elif msg.BACK in fb_msg:
            state = START_ORDER_STATE_NAME
            message = self.process_back_button(fb_msg)
        elif fb_msg == msg.WEBHOOK_EVENT:
            message = fb_msg
        else:
            state = GET_STARTED_STATE_NAME
            message = self.process_unkown_msg()

        if state:
            self.storage.set_bot_state(state)
        return message

    def add_item_to_order(self):
        item_order = models.ItemOrder.objects.get_or_create(
            item__id=self.context['item_id'],
            order__id=self.context['order_id'],
            defaults={
                'item': models.Item.objects.get(id=self.context['item_id']),
                'order': models.Order.objects.get(id=self.context['order_id']),
                'count': self.context['item_count']
            })
        self.context['item_count'] = None
        return item_order

    def process_quantity_button(self, fb_msg):
        quantity_value = fb_msg.split(':')[1]
        self.context['item_count'] = quantity_value
        item = models.Item.objects.get(id=self.context['item_id'])
        message = StartOrderState.get_select_item_msg(item, quantity_value)
        self.storage.set_bot_context(self.context)
        return message

    def process_check_order_menu(self):
        facility_info = models.Chain.objects.get(name='BSUIR BURGERS')
        item_order_records = models.ItemOrder.objects.filter(order=self.context['order_id'])
        message = CheckOrderMenuState.get_check_order_menu_msg(
            facility_info,
            item_order_records)
        return message

    def process_back_button(self, fb_msg):
        keyword = fb_msg.split(':')[1]
        if keyword == msg.ITEM_MENU:
            items = models.Item.objects.filter(
                type_of_button=self.context['type_of_button'],
                type_of_menu__category=self.context['type_of_menu'],
                type_of_menu__facility__id=self.context['facility_id'])
            message = StartOrderState.get_items_msg(items)
        elif keyword == msg.MAIN_MENU:
            menu_types = models.Menu.objects.filter(facility__id=self.context['facility_id'])
            message = StartOrderState.get_main_menu_msg(menu_types)
        return message

    def process_unkown_msg(self):
        order_id = self.context['order_id']
        if order_id:
            models.Order.objects.get(id=order_id).delete()
        self.storage.set_bot_context()
        message = State.get_unkown_msg()
        return message

    @staticmethod
    def get_change_quantity_msg():
        number_buttons = [SelectItemMenuState.make_quantity_button(number) for number in range(1, 9)]
        select_item = {
            'text': 'Сhange quantity:',
            'quick_replies': [
                *number_buttons,
                {
                    'content_type': 'text',
                    'title': 'Back',
                    'payload': f'{msg.BACK}:{msg.ITEM_MENU}'
                }
            ]
        }
        return select_item

    @staticmethod
    def make_quantity_button(number):
        elements = {
            'content_type': 'text',
            'title': number,
            'payload': f'{msg.QUANTITY_BUTTON}:{number}'
        }
        return elements
