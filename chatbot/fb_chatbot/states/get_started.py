# Copyright (c) 2019 Celadon Development LLC, All rights reserved.
# Author Hleb Serafimovich <hleb.serafimovich@celadon.ae>

from fb_chatbot.fb_api import get_user_info
from fb_chatbot import models, msg

from fb_chatbot.states.abstract import State
from fb_chatbot.states.const import (
    FIND_FACILITY_STATE_NAME,
    GET_STARTED_STATE_NAME,
    LOCATION_IMAGE_URL
)


class GetStartedState(State):
    def __init__(self, context, storage, psid):
        super().__init__(context, storage, psid)
        self.context = context
        self.storage = storage
        self.psid = psid

    def process_message(self, fb_msg):
        print('fb_msg', fb_msg)
        state = None
        user_info = get_user_info(self.psid)
        facility_info = models.Chain.objects.get(name='BSUIR BURGERS')
        if fb_msg == msg.GET_STARTED:
            message = GetStartedState.get_start_msg(user_info, facility_info)
        elif fb_msg == msg.ORDER_TO_GO:
            state = FIND_FACILITY_STATE_NAME
            message = GetStartedState.get_order_to_go_msg()
        elif fb_msg == msg.HOME:
            message = GetStartedState.get_start_msg(user_info, facility_info)
        elif fb_msg == msg.WEBHOOK_EVENT:
            message = fb_msg
        else:
            state = GET_STARTED_STATE_NAME
            message = State.get_unkown_msg()

        if state:
            self.storage.set_bot_state(state)
        return message

    # response_tamplates
    @staticmethod
    def get_start_msg(user_info, facility_info):
        get_started = {
            'attachment': {
                'type': 'template',
                'payload': {
                    'template_type': 'generic',
                    'elements': [
                        {
                            'title': f'Hi {user_info["first_name"]}! Welcome to {facility_info.name}!',
                            'image_url': facility_info.logo_url,
                            'subtitle': 'We have the right hat for everyone!',
                            'buttons': [
                                {
                                    'type': 'postback',
                                    'title': 'Order to Go',
                                    'payload': msg.ORDER_TO_GO
                                }
                            ]
                        }
                    ]
                }
            }
        }
        return get_started

    @staticmethod
    def get_order_to_go_msg():
        get_started = {
            'attachment': {
                'type': 'template',
                'payload': {
                    'template_type': 'generic',
                    'elements': [
                        {
                            'title': 'Share your location!',
                            'image_url': LOCATION_IMAGE_URL,
                            'buttons': [
                                {
                                    'type': 'postback',
                                    'title': 'Minsk',
                                    'payload': msg.MINSK
                                },
                                {
                                    'type': 'postback',
                                    'title': 'Vitebsk',
                                    'payload': msg.VITEBSK
                                },
                                {
                                    'type': 'postback',
                                    'title': 'Mogilev',
                                    'payload': msg.MOGILEV
                                },
                            ]
                        }
                    ]
                }
            }
        }
        return get_started

    @staticmethod
    def get_order_to_go_msg_old():
        order_to_go = {
            'text': 'Share your location!',
            'quick_replies': [
                {
                    'content_type': 'location'
                }
            ]
        }
        return order_to_go
