# Copyright (c) 2019 Celadon Development LLC, All rights reserved.
# Author Hleb Serafimovich <hleb.serafimovich@celadon.ae>

import factory

from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyChoice

from fb_chatbot import models


class ChainFactory(DjangoModelFactory):
    class Meta:
        model = models.Chain

    name = 'BSUIR BURGERS'
    logo_url = 'urlLogo'
    description = 'We have the right hat for everyone!'


class FacilityFactory(DjangoModelFactory):
    class Meta:
        model = models.Facility

    city = 'Minsk'
    street = 'Surganov Street'
    lat = 53.904541
    lon = 27.561523
    label = 'Surganov Street 2A, 22012 Minsk'
    chain = factory.SubFactory(ChainFactory)


class MenuFactory(DjangoModelFactory):
    class Meta:
        model = models.Menu

    category = FuzzyChoice(models.Menu.CATEGORY_CHOICES, getter=lambda c: 'main dishes')
    image_url = 'image_url'
    top_button = 'Burgers'
    midle_button = 'Sandwiches'
    bottom_button = 'Steaks & Ribs'
    facility = factory.SubFactory(FacilityFactory)


class ItemFactory(DjangoModelFactory):
    class Meta:
        model = models.Item

    name = 'Classic Burger by Alex.D'
    description = 'Traditional marbled beef burger and fresh lettuce with celadon sauce'
    image_url = 'image_url'
    price = '15.00'
    type_of_menu = factory.SubFactory(MenuFactory)
    type_of_button = FuzzyChoice(models.Item.BUTTON_CHOICES, getter=lambda c: 'top')
