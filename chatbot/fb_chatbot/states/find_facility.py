# Copyright (c) 2019 Celadon Development LLC, All rights reserved.
# Author Hleb Serafimovich <hleb.serafimovich@celadon.ae>

from geopy.distance import vincenty

from fb_chatbot import models, msg

from fb_chatbot.states.abstract import State
from fb_chatbot.states.const import (
    GET_STARTED_STATE_NAME,
    START_ORDER_STATE_NAME
)


class FindFacilityState(State):
    def __init__(self, context, storage, psid):
        super().__init__(context, storage, psid)
        self.context = context
        self.storage = storage

    def process_message(self, fb_msg):
        state = None
        if msg.MINSK in fb_msg:
            message, state = FindFacilityState.process_get_location_button(fb_msg)
        elif fb_msg == msg.WEBHOOK_EVENT:
            message = fb_msg
        elif msg.USER_TAG in fb_msg:
            message, state = FindFacilityState.process_input_location_msg(fb_msg)
        else:
            state = GET_STARTED_STATE_NAME
            message = State.get_unkown_msg()

        if state:
            self.storage.set_bot_state(state)
        return message

    @staticmethod
    def process_get_location_button(fb_msg):
        facilities = []
        facility_info = models.Chain.objects.get(name='BSUIR BURGERS')
        user_lat, user_lon = 53, 54
        facility = models.Facility.objects.all()
        for value in facility:
            facility_lat = value.lat
            facility_lon = value.lon
            distance = vincenty((user_lat, user_lon), (facility_lat, facility_lon)).kilometers
            if distance <= 20:
                facilities.append(value)
            if not facilities:
                state = GET_STARTED_STATE_NAME
                message = FindFacilityState.get_no_facility_nearby_msg(facility_info)
            else:
                state = START_ORDER_STATE_NAME
                message = FindFacilityState.get_facilities_msg(facilities)
        return message, state

    @staticmethod
    def process_input_location_msg(fb_msg):
        fb_msg = fb_msg.split(':')[1].strip()
        facility_info = models.Chain.objects.get(name='BSUIR BURGERS')
        facilities = models.Facility.objects.filter(city__iexact=fb_msg)
        if not facilities:
            state = GET_STARTED_STATE_NAME
            message = FindFacilityState.get_no_facility_nearby_msg(facility_info)
        else:
            state = START_ORDER_STATE_NAME
            message = FindFacilityState.get_facilities_msg(facilities)
        return message, state

    # response_tamplates
    @staticmethod
    def get_facilities_msg(facilities):
        facilities = {
            'attachment': {
                'type': 'template',
                'payload': {
                    'template_type': 'generic',
                    'elements': [FindFacilityState.make_facility_list(facility) for facility in facilities]
                }
            }
        }
        return facilities

    @staticmethod
    def make_facility_list(facility):
        elements = {
            'title': facility.street,
            'subtitle': facility.label,
            'buttons': [
                {
                    'type': 'postback',
                    'title': 'Start Order',
                    'payload': f'{msg.SELECT_FACILITY}:{facility.id}'
                }
            ]
        }
        return elements

    @staticmethod
    def get_no_facility_nearby_msg(facility_info):
        no_facility = {
            'attachment': {
                'type': 'template',
                'payload': {
                    'template_type': 'generic',
                    'elements': [
                        {
                            'title': 'No stores found',
                            'image_url': facility_info.logo_url,
                            'subtitle': 'Please try a different search',
                            'buttons': [
                                {
                                    'type': 'postback',
                                    'title': 'Order to Go',
                                    'payload': msg.ORDER_TO_GO
                                },
                                {
                                    'type': 'postback',
                                    'title': 'Contact us',
                                    'payload': 'DEVELOPER_DEFINED_PAYLOAD'
                                }
                            ]
                        }
                    ]
                }
            }
        }
        return no_facility
