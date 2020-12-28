# Copyright (c) 2019 Celadon Development LLC, All rights reserved.
# Author Hleb Serafimovich <hleb.serafimovich@celadon.ae>

from django.contrib.postgres.fields import JSONField
from django.db import models


class BotState(models.Model):
    class Meta:
        db_table = 'BotState'

    psid = models.BigIntegerField(
        primary_key=True,
        unique=True,
        db_index=True,
    )

    state = models.CharField(
        max_length=255,
        db_index=True
    )

    context = JSONField(default=dict)


class Chain(models.Model):
    class Meta:
        db_table = 'Chain'

    name = models.CharField(
        max_length=255,
        db_index=True
    )

    logo_url = models.CharField(
        max_length=255,
        db_index=True
    )

    description = models.CharField(
        max_length=255,
        db_index=True
    )

    def __str__(self):
        return self.name


class Facility(models.Model):
    class Meta:
        db_table = 'Facility'
        verbose_name = 'Facility'
        verbose_name_plural = 'Facilities'

    city = models.CharField(
        max_length=255,
        db_index=True
    )

    street = models.CharField(
        max_length=255,
        db_index=True
    )

    label = models.CharField(
        max_length=255,
        db_index=True
    )

    lat = models.DecimalField(
        max_digits=8,
        decimal_places=6,
        db_index=True
    )

    lon = models.DecimalField(
        max_digits=8,
        decimal_places=6,
        db_index=True
    )

    chain = models.ForeignKey(
        'fb_chatbot.Chain',
        on_delete=models.CASCADE,
        null=False,
        db_index=True,
    )

    def __str__(self):
        return f'facility from {self.label}'


class Menu(models.Model):
    class Meta:
        db_table = 'Menu'
        verbose_name = 'Menu'
        verbose_name_plural = 'Menu types'

    CATEGORY_CHOICES = (
        ('main dishes', 'Main dishes'),
        ('snacks', 'Snacks'),
        ('desserts', 'Desserts'),
        ('drinks', 'Drinks')
    )

    category = models.CharField(
        max_length=255,
        choices=CATEGORY_CHOICES,
        db_index=True
    )

    image_url = models.CharField(
        max_length=255,
        db_index=True
    )

    top_button = models.CharField(
        max_length=255,
        db_index=True
    )

    midle_button = models.CharField(
        max_length=255,
        db_index=True
    )

    bottom_button = models.CharField(
        max_length=255,
        db_index=True
    )

    facility = models.ForeignKey(
        'fb_chatbot.Facility',
        on_delete=models.CASCADE,
        null=False,
        db_index=True,
    )

    def __str__(self):
        return f'{self.category} Menu for {self.facility}'


class Item(models.Model):
    class Meta:
        db_table = 'Item'

    name = models.CharField(
        max_length=255,
        db_index=True
    )

    description = models.CharField(
        max_length=255,
        db_index=True
    )

    image_url = models.CharField(
        max_length=255,
        db_index=True
    )

    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        db_index=True
    )

    BUTTON_CHOICES = (
        ('top', 'Top'),
        ('midle', 'Midle'),
        ('bottom', 'Bottom')
    )

    type_of_menu = models.ForeignKey(
        'fb_chatbot.Menu',
        on_delete=models.CASCADE,
        null=False,
        db_index=True,
    )

    type_of_button = models.CharField(
        max_length=255,
        choices=BUTTON_CHOICES,
        verbose_name='Type of Button on the main menu',
        db_index=True
    )

    def __str__(self):
        return f'{self.name}'


class Order(models.Model):
    class Meta:
        db_table = 'Order'

    psid = models.ForeignKey(
        'fb_chatbot.BotState',
        on_delete=models.CASCADE,
        null=False,
        db_index=True
    )

    facility = models.ForeignKey(
        'fb_chatbot.Facility',
        on_delete=models.CASCADE,
        null=False,
        db_index=True,
    )

    items = models.ManyToManyField(
        'fb_chatbot.Item',
        through='ItemOrder',
        db_index=True
    )

    STATUS_CHOICES = (
        ('in process', 'In process'),
        ('paid', 'Paid'),
        ('cooking', 'Cooking'),
        ('ready', 'Ready'),
        ('given away', 'Given away'),
        ('canceled', 'Canceled')
    )

    status = models.CharField(
        max_length=255,
        choices=STATUS_CHOICES,
        db_index=True
    )

    # customer = models.ForeignKey(
    #     'payment.Customer',
    #     on_delete=models.CASCADE,
    #     null=True,
    #     db_index=True
    # )

    created = models.DateTimeField(auto_now_add=True)


class ItemOrder(models.Model):
    class Meta:
        db_table = 'ItemOrder'

    item = models.ForeignKey(
        'fb_chatbot.Item',
        on_delete=models.CASCADE,
        null=False,
        db_index=True,
    )

    order = models.ForeignKey(
        'fb_chatbot.Order',
        on_delete=models.CASCADE,
        null=False,
        db_index=True,
    )

    count = models.IntegerField(
        db_index=True,
        default=0,
        null=False
    )
