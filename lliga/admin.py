from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Lliga)
admin.site.register(Equip)
admin.site.register(Jugador)
admin.site.register(Fitxa)
admin.site.register(Partit)
admin.site.register(Event)

