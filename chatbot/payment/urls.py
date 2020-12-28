# Copyright (c) 2019 Celadon Development LLC, All rights reserved.
# Author Hleb Serafimovich <hleb.serafimovich@celadon.ae>

from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from payment import views


app_name = 'payment'

urlpatterns = [
    path('home/', csrf_exempt(views.HomePage.as_view()), name='home_page'),
    path('registration/', csrf_exempt(views.Registration.as_view()), name='registration'),
    path('login/', csrf_exempt(views.Login.as_view()), name='login'),
    path('logout/', views.loggout, name='logout'),
]
