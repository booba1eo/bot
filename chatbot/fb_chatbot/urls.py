# Copyright (c) 2019 Celadon Development LLC, All rights reserved.
# Author Hleb Serafimovich <hleb.serafimovich@celadon.ae>

from django.urls import path

from fb_chatbot.views import ChatBotView

urlpatterns = [
    path('webhook/', ChatBotView.as_view(), name='chatbot'),
]
