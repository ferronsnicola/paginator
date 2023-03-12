from django.contrib import admin
from django.apps import apps

# Register your models here.
for model in apps.get_app_config('playing_cards_paginator').get_models():
    admin.site.register(model)