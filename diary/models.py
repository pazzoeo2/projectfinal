from django.db import models
from django.conf import settings

# Create your models here.

class Game(models.Model):
    name = models.CharField(max_length=100)
    cover = models.CharField(max_length=200, blank=True)

class Entry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    started = models.DateField(blank=True, null=True)
    finished = models.DateField(blank=True, null=True)
    timeplayed = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=20, blank=True)
    review = models.CharField(max_length=1000, blank=True)