# Copyright (c) 2019 Celadon Development LLC, All rights reserved.
# Author Hleb Serafimovich <hleb.serafimovich@celadon.ae>

from fb_chatbot.models import BotState

from fb_chatbot.states.const import GET_STARTED_STATE_NAME


class StateStorage():
    context_default = {
        'facility_id': None,
        'order_id': None,
        'item_id': None,
        'type_of_menu': None,
        'type_of_button': None,
        'item_count': None
    }

    def __init__(self, psid):
        self.psid = psid

    def get_bot_state(self):
        user = BotState.objects.get_or_create(
            psid=self.psid,
            defaults={
                'state': GET_STARTED_STATE_NAME,
                'context': self.context_default}
        )[0]

        return user.state, user.context

    def set_bot_state(self, state_value):
        BotState.objects.filter(psid=self.psid).update(state=state_value)

    def set_bot_context(self, context_value=None):
        if context_value is None:
            context_value = self.context_default
        BotState.objects.filter(psid=self.psid).update(context=context_value)
