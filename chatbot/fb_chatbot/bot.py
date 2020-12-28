# Copyright (c) 2019 Celadon Development LLC, All rights reserved.
# Author Hleb Serafimovich <hleb.serafimovich@celadon.ae>

from fb_chatbot import msg
from fb_chatbot.bot_storage import StateStorage

from fb_chatbot.states import make_state


class Bot:
    def __init__(self, psid):
        self.storage = StateStorage(psid)
        self.state = None
        self.psid = psid

    def handle_response_message(self, fb_msg):
        message = self.process_message(fb_msg)
        if isinstance(message, list):
            response_msg = [{'recipient': {'id': self.psid}, 'message': msg} for msg in message]
        else:
            response_msg = {'recipient': {'id': self.psid}, 'message': message}
            if message == msg.WEBHOOK_EVENT:
                response_msg = message
        return response_msg

    def process_message(self, fb_msg):
        state, context = self.storage.get_bot_state()
        self.state = make_state(state, context, self.storage, self.psid)
        message = self.state.process_message(fb_msg)
        return message
