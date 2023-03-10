from django.contrib import admin

# Register your models here.

from .models import *

class LligaAdmin(admin.ModelAdmin):
	filter_horizontal = ["equips"]
admin.site.register(Lliga,LligaAdmin)

admin.site.register(Equip)
admin.site.register(Jugador)
admin.site.register(Fitxa)
admin.site.register(Partit)


class EventAdmin(admin.ModelAdmin):
	list_display = ["partit","temps","tipus","equip","jugador"]
admin.site.register(Event,EventAdmin)

