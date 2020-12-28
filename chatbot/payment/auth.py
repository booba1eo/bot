# Copyright (c) 2019 Celadon Development LLC, All rights reserved.
# Author Hleb Serafimovich <hleb.serafimovich@celadon.ae>

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class CustomBackend:
    AUTH_FIELD = None

    def get_user_qs(self, user_model, username):
        return user_model.objects.get(**{self.AUTH_FIELD: username})

    def authenticate(self, request=None, username=None, password=None):
        user_model = get_user_model()

        try:
            user = self.get_user_qs(user_model, username)
        except user_model.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None


class UsernameAuthBackend(CustomBackend, ModelBackend):
    AUTH_FIELD = 'username'
