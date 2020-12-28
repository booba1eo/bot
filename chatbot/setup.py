# Copyright (c) 2019 Celadon Development LLC, All rights reserved.
# Author Hleb Serafimovich <hleb.serafimovich@celadon.ae>

import os
from setuptools import setup, find_packages

setup(
    name='chatbot',
    version=os.getenv('BOT_VERSION') or os.getenv('BITBUCKET_COMMIT'),
    url='https://bitbucket.org/celadonteam/bot/src/master/',
    description='test chatbot for facebook',
    packages=find_packages(),
    install_requires=[
        'Django==2.2',
        'djangorestframework==3.9.2',
        'requests==2.21.0',
        'psycopg2-binary==2.8.2',
        'pytz==2019.1',
        'geopy==1.20.0',
        'uWSGI==2.0.18'
    ],
    include_package_data=True,
    scripts=['manage.py', ]
)
