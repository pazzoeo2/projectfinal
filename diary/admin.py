from django.contrib import admin
from .models import DailyPlaytime, Entry, Game

# Register your models here.

admin.site.register(Entry)
admin.site.register(Game)
admin.site.register(DailyPlaytime)
