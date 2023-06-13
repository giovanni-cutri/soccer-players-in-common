from django.db import models

# Create your models here.

class Team(models.Model):
    name = models.CharField(max_length=64)
    image = models.URLField(max_length=200)
    link = models.URLField(max_length=200)
