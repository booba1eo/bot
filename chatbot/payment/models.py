# Copyright (c) 2019 Celadon Development LLC, All rights reserved.
# Author Hleb Serafimovich <hleb.serafimovich@celadon.ae>

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Meta:
        db_table = 'User'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    first_name = models.CharField(
        max_length=30,
        blank=False,
    )

    last_name = models.CharField(
        max_length=30,
        blank=False,
    )

    email = models.CharField(
        max_length=30,
        blank=False,
    )

    mobile_number = models.BigIntegerField(
        db_index=True,
        null=True,
    )

    birthday = models.DateField(
        db_index=True,
        null=True,
    )

    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
    )

    gender = models.CharField(
        max_length=50,
        choices=GENDER_CHOICES,
        db_index=True,
        null=True,
    )

    abandoned_basket = models.CharField(
        max_length=255,
        db_index=True,
        null=True,
        blank=True,
    )

    lost_basket = models.CharField(
        max_length=255,
        db_index=True,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f'{self.username}'
