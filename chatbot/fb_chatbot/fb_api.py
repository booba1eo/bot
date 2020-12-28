# Copyright (c) 2019 Celadon Development LLC, All rights reserved.
# Author Hleb Serafimovich <hleb.serafimovich@celadon.ae>

import json
import logging
import os
import requests

from fb_chatbot.facebook_api_properties import SET_PROPERTIES, DELETE_PROPERTIES

ENDPOINT = 'https://graph.facebook.com/v3.3'
PAGE_ACCESS_TOKEN = os.environ['BOT_PAGE_ACCESS_TOKEN']


def post_message(message=None):
    if isinstance(message, list):
        for value in message:
            handle_post_message(value)
    else:
        handle_post_message(message)


def handle_post_message(message=None):
    post_message_url = f'{ENDPOINT}/me/messages'
    payload = {'access_token': PAGE_ACCESS_TOKEN}
    response_msg = json.dumps(message)
    print('response_msg', response_msg)
    status = requests.post(
        post_message_url,
        params=payload,
        headers={'Content-Type': 'application/json'},
        data=response_msg)
    status.raise_for_status()
    logging.debug(status.json())
    return status.json()


def post_sender_action(psid):
    post_message_url = f'{ENDPOINT}/me/messages'
    payload = {'access_token': PAGE_ACCESS_TOKEN}
    response_msg = json.dumps({'recipient': {'id': psid}, 'sender_action': 'typing_on'})
    status = requests.post(
        post_message_url,
        params=payload,
        headers={'Content-Type': 'application/json'},
        data=response_msg)
    status.raise_for_status()
    logging.debug(status.json())
    return status.json()


def set_property(profile_property):
    post_message_url = f'{ENDPOINT}/me/messenger_profile'
    payload = {'access_token': PAGE_ACCESS_TOKEN}
    msg = json.dumps(SET_PROPERTIES[profile_property])
    status = requests.post(
        post_message_url,
        params=payload,
        headers={'Content-Type': 'application/json'},
        data=msg)
    status.raise_for_status()
    logging.debug(status.json())


def delete_property():
    post_message_url = f'{ENDPOINT}/me/messenger_profile'
    payload = {'access_token': PAGE_ACCESS_TOKEN}
    msg = json.dumps({
        'fields': DELETE_PROPERTIES
    })
    status = requests.delete(
        post_message_url,
        params=payload,
        headers={'Content-Type': 'application/json'},
        data=msg)
    status.raise_for_status()
    logging.debug(status.json())


def get_user_info(psid):
    post_message_url = f'{ENDPOINT}/{psid}'
    payload = {'fields': 'first_name', 'access_token': PAGE_ACCESS_TOKEN}
    status = requests.get(
        post_message_url,
        params=payload,
        headers={'Content-Type': 'application/json'})
    status.raise_for_status()
    logging.debug(status.json())
    return status.json()
