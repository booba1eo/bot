# Copyright (c) 2019 Celadon Development LLC, All rights reserved.
# Author Hleb Serafimovich <hleb.serafimovich@celadon.ae>

import json
import logging
import os

from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

from fb_chatbot import fb_api, msg
from fb_chatbot.bot import Bot


VERIFY_TOKEN = os.environ['BOT_VERIFY_TOKEN']


class ChatBotView(generic.View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        # hub_mode  = request.GET.get('hub.mode')
        hub_token = request.GET.get('hub.verify_token')
        hub_challenge = request.GET.get('hub.challenge')
        if hub_token != VERIFY_TOKEN:
            return HttpResponse('Error, invalid token')
        return HttpResponse(hub_challenge)

    def post(self, request, *args, **kwargs):
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        assert len(incoming_message['entry']) == 1
        assert len(incoming_message['entry'][0]['messaging']) == 1
        psid, fb_msg = ChatBotView.parse_incoming_message(incoming_message)
        bot = Bot(psid)
        response_msg = bot.handle_response_message(fb_msg)
        if response_msg == msg.WEBHOOK_EVENT:
            return HttpResponse('Success', status=200)
        if psid and response_msg:
            fb_api.post_sender_action(psid)
            fb_api.post_message(response_msg)
            return HttpResponse('Success', status=200)
        return HttpResponse('Failed', status=400)

    @staticmethod
    def parse_incoming_message(incoming_message):
        for entry in incoming_message['entry']:
            for messaging in entry['messaging']:
                psid = messaging['sender']['id']
                if 'message' in messaging:
                    fb_msg = ChatBotView.parse_message_type(messaging)
                elif 'postback' in messaging:
                    fb_msg = messaging['postback']['payload']
                elif ('read' in messaging) or ('delivery' in messaging):
                    fb_msg = msg.WEBHOOK_EVENT
                else:
                    fb_msg = msg.UNKNOWN
                return psid, fb_msg

    @staticmethod
    def parse_message_type(messaging):
        if 'attachments' in messaging['message']:
            for attachments in messaging['message']['attachments']:
                if 'coordinates' in attachments['payload']:
                    fb_msg = attachments['payload']['coordinates']
                    logging.debug(fb_msg)
                else:
                    fb_msg = msg.UNKNOWN
        elif 'quick_reply' in messaging['message']:
            fb_msg = messaging['message']['quick_reply']['payload']
        else:
            fb_msg = messaging['message'].get('text')
            fb_msg = f'{msg.USER_TAG}:{fb_msg}'
        return fb_msg
