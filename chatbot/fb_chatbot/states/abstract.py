# Copyright (c) 2019 Celadon Development LLC, All rights reserved.
# Author Hleb Serafimovich <hleb.serafimovich@celadon.ae>

from abc import ABCMeta, abstractmethod

from fb_chatbot import msg


class State(metaclass=ABCMeta):
    name = 'abstact'
    @abstractmethod
    def __init__(self, context, storage, psid):
        pass

    @abstractmethod
    def process_message(self, fb_msg):
        pass

    @staticmethod
    def get_unkown_msg():
        unknown = {
            'attachment': {
                'type': 'template',
                'payload': {
                    'template_type': 'generic',
                    'elements': [
                        {
                            'title': 'I do not understand you!',
                            'buttons': [
                                {
                                    'type': 'postback',
                                    'title': 'Home',
                                    'payload': msg.HOME
                                }
                            ]
                        }
                    ]
                }
            }
        }
        return unknown
