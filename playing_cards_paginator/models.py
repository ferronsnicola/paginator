from django.db import models


# Create your models here.
class BackFile(models.Model):
    back = models.FileField(upload_to='documents/backs')


class FrontFiles(models.Model):
    front = models.FileField(upload_to='documents/fronts')


