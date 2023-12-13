from django.contrib import admin

from Game.models import *

# Register your models here.
admin.site.register(Game)
admin.site.register(Cell)
admin.site.register(Grid)