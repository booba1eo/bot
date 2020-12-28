# Copyright (c) 2019 Celadon Development LLC, All rights reserved.
# Author Hleb Serafimovich <hleb.serafimovich@celadon.ae>

SET_PROPERTIES = {
    'get started button': {
        'get_started': {'payload': 'GET_STARTED'}
    },
    'greeting text': {
        'greeting': [
            {
                'locale': 'default',
                'text': 'Hello {{user_first_name}}!'
            }
        ]
    }

}

DELETE_PROPERTIES = [
    'account_linking_url',
    'persistent_menu',
    'get_started',
    'greeting',
    'whitelisted_domains',
    'target_audience',
    'home_url'
]
