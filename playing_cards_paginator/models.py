from django.db import models
import json


def dynamic_path(instance, filename):
    return f'documents/{instance.session_id}/{instance.base_dir}/{instance.deck_name}/{filename}'


class CardFile(models.Model):
    base_dir = models.CharField(max_length=255)
    session_id = models.CharField(max_length=255)
    deck_name = models.CharField(max_length=255)
    file = models.FileField(upload_to=dynamic_path)
    short_name = models.CharField(max_length=255)
