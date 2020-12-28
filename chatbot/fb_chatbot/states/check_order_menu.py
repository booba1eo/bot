# Copyright (c) 2019 Celadon Development LLC, All rights reserved.
# Author Hleb Serafimovich <hleb.serafimovich@celadon.ae>

import os

from django.urls import reverse

from fb_chatbot import models, msg
from fb_chatbot.fb_api import get_user_info

from fb_chatbot.states.abstract import State
from fb_chatbot.states.get_started import GetStartedState
from fb_chatbot.states.start_order import StartOrderState


class CheckOrderMenuState(State):
    def __init__(self, context, storage, psid):
        super().__init__(context, storage, psid)
        self.context = context
        self.storage = storage
        self.psid = psid

    def process_message(self, fb_msg):
        state = None
        if fb_msg == msg.ADD_MORE_ITEMS:
            state = StartOrderState.__name__
            menu_types = models.Menu.objects.filter(facility__id=self.context['facility_id'])
            message = StartOrderState.get_main_menu_msg(menu_types)
        elif msg.REMOVE_ITEM in fb_msg:
            message, state = self.process_remove_item_button(fb_msg)
        elif fb_msg == msg.CANCEL_ORDER:
            state = GetStartedState.__name__
            message = self.process_cancel_order_button()
        elif fb_msg == msg.WEBHOOK_EVENT:
            message = fb_msg
        else:
            state = GetStartedState.__name__
            models.Order.objects.get(id=self.context['order_id']).delete()
            self.storage.set_bot_context()
            message = State.get_unkown_msg()

        if state:
            self.storage.set_bot_state(state)
        return message

    def process_remove_item_button(self, fb_msg):
        id_value = fb_msg.split(':')[1]
        item_order_records = models.ItemOrder.objects.all()
        item_order_records.get(id=id_value).delete()
        if item_order_records:
            state = CheckOrderMenuState.__name__
            message = self.process_check_order_menu()
        else:
            state = StartOrderState.__name__
            menu_types = models.Menu.objects.filter(facility__id=self.context['facility_id'])
            message = StartOrderState.get_main_menu_msg(menu_types)
        return message, state

    def process_cancel_order_button(self):
        models.Order.objects.get(id=self.context['order_id']).delete()
        self.storage.set_bot_context()
        user_info = get_user_info(self.psid)
        facility_info = models.Chain.objects.get(name='BSUIR BURGERS')
        message = GetStartedState.get_start_msg(user_info, facility_info)
        return message

    def process_check_order_menu(self):
        facility_info = models.Chain.objects.get(name='BSUIR BURGERS')
        item_order_records = models.ItemOrder.objects.filter(order=self.context['order_id'])
        message = CheckOrderMenuState.get_check_order_menu_msg(
            facility_info,
            item_order_records)
        return message

    @staticmethod
    def get_check_order_menu_msg(facility_info, item_order_records):
        items = [CheckOrderMenuState.make_items(item_in_order) for item_in_order in item_order_records]
        url = reverse('payment:home_page')
        webview_url = os.environ['BOT_WEBVIEW_DOMAIN'] + url
        message = {
            'attachment': {
                'type': 'template',
                'payload': {
                    'template_type': 'generic',
                    'elements': [
                        {
                            'title': 'Order Summary',
                            'subtitle': 'price',
                            'image_url': facility_info.logo_url,
                            'buttons': [
                                {
                                    'type': 'web_url',
                                    'url': webview_url,
                                    'messenger_extensions': 'true',
                                    'webview_height_ratio': 'compact',
                                    'title': 'Check out online',
                                    'payload': msg.ADD_MORE_ITEMS
                                },
                                {
                                    'type': 'postback',
                                    'title': 'Add more items',
                                    'payload': msg.ADD_MORE_ITEMS
                                }
                            ]
                        },
                        *items,
                        {
                            'title': 'More options',
                            'image_url': facility_info.logo_url,
                            'buttons': [
                                {
                                    'type': 'postback',
                                    'title': 'Cancel order',
                                    'payload': msg.CANCEL_ORDER
                                }
                            ]
                        }
                    ]
                }
            }
        }
        return message

    @staticmethod
    def make_items(item_in_order):
        items = {
            'title': f'({item_in_order.count}x) {item_in_order.item.name} {item_in_order.item.price}$',
            'subtitle': item_in_order.item.description,
            'image_url': item_in_order.item.image_url,
            'buttons': [
                {
                    'type': 'postback',
                    'title': 'Remove',
                    'payload': f'{msg.REMOVE_ITEM}:{item_in_order.id}'
                }
            ]
        }
        return items
