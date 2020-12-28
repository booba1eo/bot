# Copyright (c) 2019 Celadon Development LLC, All rights reserved.
# Author Hleb Serafimovich <hleb.serafimovich@celadon.ae>

from django.contrib import admin

from fb_chatbot import models


admin.site.register(models.BotState)
admin.site.register(models.Chain)
admin.site.register(models.Facility)
admin.site.register(models.Menu)
admin.site.register(models.Item)
admin.site.register(models.Order)
admin.site.register(models.ItemOrder)
