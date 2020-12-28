# Copyright (c) 2019 Celadon Development LLC, All rights reserved.
# Author Hleb Serafimovich <hleb.serafimovich@celadon.ae>

from fb_chatbot.states.abstract import State
from fb_chatbot.states.get_started import GetStartedState
from fb_chatbot.states.find_facility import FindFacilityState
from fb_chatbot.states.start_order import StartOrderState
from fb_chatbot.states.select_item import SelectItemMenuState
from fb_chatbot.states.check_order_menu import CheckOrderMenuState


STATES = {
    GetStartedState.__name__: GetStartedState,
    FindFacilityState.__name__: FindFacilityState,
    StartOrderState.__name__: StartOrderState,
    SelectItemMenuState.__name__: SelectItemMenuState,
    CheckOrderMenuState.__name__: CheckOrderMenuState
}


def make_state(state, context, storage, psid):
    state_class = STATES[state]
    state = state_class(context, storage, psid)
    return state