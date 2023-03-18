from django.db import models
import json


def dynamic_path(instance, filename):
    return f'documents/{instance.session_id}/{instance.base_dir}/{instance.group_name}/{filename}'



# Create your models here.
class BackFile(models.Model):
    base_dir = 'backs'
    session_id = models.CharField(max_length=255)
    group_name = models.CharField(max_length=255)
    back = models.FileField(upload_to=dynamic_path)
    short_name = models.CharField(max_length=255)


class FrontFiles(models.Model):
    base_dir = 'fronts'
    session_id = models.CharField(max_length=255)
    group_name = models.CharField(max_length=255)
    front = models.FileField(upload_to=dynamic_path)
    short_name = models.CharField(max_length=255)


