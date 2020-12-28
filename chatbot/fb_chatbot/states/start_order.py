# Copyright (c) 2019 Celadon Development LLC, All rights reserved.
# Author Hleb Serafimovich <hleb.serafimovich@celadon.ae>

from fb_chatbot import models, msg

from fb_chatbot.states.abstract import State
from fb_chatbot.states.const import (
    SELECT_ITEM_STATE_NAME,
    GET_STARTED_STATE_NAME
)


class StartOrderState(State):
    def __init__(self, context, storage, psid):
        super().__init__(context, storage, psid)
        self.context = context
        self.storage = storage
        self.psid = psid

    def process_message(self, fb_msg):
        state = None
        print('~~~~~~~~~~~~~~~~~~')
        print('fb_msg', fb_msg)
        print('~~~~~~~~~~~~~~~~~~')

        if msg.SELECT_FACILITY in fb_msg:
            message = self.process_select_facility_button(fb_msg)
        elif ',' in fb_msg:
            message = self.process_items_menu(fb_msg)
        elif msg.SELECT_ITEM in fb_msg:
            state = SELECT_ITEM_STATE_NAME
            message = self.process_select_item_button(fb_msg)
        elif msg.BACK in fb_msg:
            message = self.process_back_button(fb_msg)
        elif fb_msg == msg.WEBHOOK_EVENT:
            message = fb_msg
        else:
            state = GET_STARTED_STATE_NAME
            message = self.process_unkown_msg()

        if state:
            self.storage.set_bot_state(state)
        return message

    # Process button
    def process_select_facility_button(self, fb_msg):
        id_value = fb_msg.split(':')[1]
        self.context['facility_id'] = id_value
        menu_types = models.Menu.objects.filter(facility__id=id_value)
        message = StartOrderState.get_main_menu_msg(menu_types)
        self.storage.set_bot_context(self.context)
        return message

    def process_select_item_button(self, fb_msg):
        id_value = fb_msg.split(':')[1]
        item = models.Item.objects.get(id=id_value)
        self.context['item_id'] = item.id
        self.context['item_count'] = 1
        check_user_orders = models.Order.objects.filter(
            psid=self.psid,
            status=models.Order.STATUS_CHOICES[0][0])
        if not check_user_orders:
            order = self.make_order()
            self.context['order_id'] = order.id
        message = StartOrderState.get_select_item_msg(item, self.context['item_count'])
        self.storage.set_bot_context(self.context)
        return message

    # Item msg
    def process_items_menu(self, fb_msg):
        type_of_menu, type_of_button = fb_msg.split(',')
        self.context['type_of_menu'] = type_of_menu
        self.context['type_of_button'] = type_of_button
        items = models.Item.objects.filter(
            type_of_button=type_of_button,
            type_of_menu__category=type_of_menu,
            type_of_menu__facility__id=self.context['facility_id'])
        if not items:
            message = StartOrderState.get_no_items_msg()
        else:
            message = StartOrderState.get_items_msg(items)

        self.storage.set_bot_context(self.context)
        return message

    # Order func
    def make_order(self):
        order = models.Order.objects.create(
            psid=models.BotState.objects.get(psid=self.psid),
            facility=models.Facility.objects.get(id=self.context['facility_id']),
            status=models.Order.STATUS_CHOICES[0][0])
        return order

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

    # response_tamplates
    @staticmethod
    def get_main_menu_msg(menu_types):
        menu = {
            'attachment': {
                'type': 'template',
                'payload': {
                    'template_type': 'generic',
                    'elements': [StartOrderState.make_main_menu(menu) for menu in menu_types]
                }
            }
        }
        return menu

    @staticmethod
    def make_main_menu(menu):
        elements = {
            'title': 'What would you like to order?',
            'image_url': menu.image_url,
            'buttons': [
                {
                    'type': 'postback',
                    'title': menu.top_button,
                    'payload': f'{menu.category},top'
                },
                {
                    'type': 'postback',
                    'title': menu.midle_button,
                    'payload': f'{menu.category},midle'
                },
                {
                    'type': 'postback',
                    'title': menu.bottom_button,
                    'payload': f'{menu.category},bottom'
                }
            ]
        }
        return elements

    @staticmethod
    def get_items_msg(item_list):
        item = {
            'attachment': {
                'type': 'template',
                'payload': {
                    'template_type': 'generic',
                    'elements': [StartOrderState.make_items_in_menu(item) for item in item_list]
                }
            }
        }
        return item

    @staticmethod
    def make_items_in_menu(item):
        elements = {
            'title': f'{item.name} {item.price}$',
            'subtitle': item.description,
            'image_url': item.image_url,
            'buttons': [
                {
                    'type': 'postback',
                    'title': 'Select',
                    'payload': f'{msg.SELECT_ITEM}:{item.id}'
                },
                {
                    'type': 'postback',
                    'title': 'Back',
                    'payload': f'{msg.BACK}:{msg.MAIN_MENU}'
                }
            ]
        }
        return elements

    @staticmethod
    def get_no_items_msg():
        no_item = {
            'attachment': {
                'type': 'template',
                'payload': {
                    'template_type': 'generic',
                    'elements': [
                        {
                            'title': 'Unfortunately, there is nothing in this menu available.',
                            'buttons': [
                                {
                                    'type': 'postback',
                                    'title': 'Back',
                                    'payload': f'{msg.BACK}:{msg.MAIN_MENU}'
                                }
                            ]
                        }
                    ]
                }
            }
        }
        return no_item

    @staticmethod
    def get_select_item_msg(item, count):
        select_item = {
            'text': f'Ok! You selected ({count}x){item.name}!',
            'quick_replies': [
                {
                    'content_type': 'text',
                    'title': 'Add to order',
                    'payload': msg.ADD_ITEM_TO_ORDER
                },
                {
                    'content_type': 'text',
                    'title': f'Change quantity ({count})',
                    'payload': msg.CHANGE_QUANTITY_ITEM
                },
                {
                    'content_type': 'text',
                    'title': 'Back',
                    'payload': f'{msg.BACK}:{msg.ITEM_MENU}'
                }
            ]
        }
        return select_item
