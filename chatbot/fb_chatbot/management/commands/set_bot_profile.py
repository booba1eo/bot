# Copyright (c) 2019 Celadon Development LLC, All rights reserved.
# Author Hleb Serafimovich <hleb.serafimovich@celadon.ae>

from django.core.management.base import BaseCommand

from fb_chatbot.fb_api import set_property, delete_property
from fb_chatbot.facebook_api_properties import SET_PROPERTIES


class Command(BaseCommand):
    # pylint: disable=W0612,W0613
    help = 'Set bot profile'

    def handle(self, *args, **kwargs):
        delete_property()
        for value in SET_PROPERTIES:
            set_property(value)
