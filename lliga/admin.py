from django.contrib import admin

# Register your models here.

from .models import *

class LligaAdmin(admin.ModelAdmin):
    filter_horizontal = ["equips"]
admin.site.register(Lliga,LligaAdmin)

admin.site.register(Equip)
admin.site.register(Jugador)
admin.site.register(Fitxa)


class EventInline(admin.TabularInline):
    model = Event
    fields = ["temps","tipus","jugador","equip"]
    ordering = ("temps",)
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "jugador":
            partit_id = request.resolver_match.kwargs['object_id']
            partit = Partit.objects.get(id=partit_id)
            jugadors_local = [fitxa.jugador.id for fitxa in partit.local.fitxa_set.all()]
            jugadors_visitant = [fitxa.jugador.id for fitxa in partit.visitant.fitxa_set.all()]
            jugadors = jugadors_local + jugadors_visitant
            kwargs["queryset"] = Jugador.objects.filter(id__in=jugadors)
        elif db_field.name == "equip":
            partit_id = request.resolver_match.kwargs['object_id']
            partit = Partit.objects.get(id=partit_id)
            equips = [ partit.local.id, partit.visitant.id ]
            kwargs["queryset"] = Equip.objects.filter(id__in=equips)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)            
class PartitAdmin(admin.ModelAdmin):
        # podem fer cerques en els models relacionats
        # (noms dels equips o títol de la lliga)
    search_fields = ["local__nom","visitant__nom","lliga__titol"]
        # el camp personalitzat ("resultats" o recompte de gols)
        # el mostrem com a "readonly_field"
    readonly_fields = ["resultat",]
    list_display = ["local","visitant","resultat","lliga","inici"]
    ordering = ("-inici",)
    inlines = [EventInline,]
    def resultat(self,obj):
        gols_local = obj.event_set.filter(
                        tipus=Event.EventType.GOL,
                                equip=obj.local).count()
        gols_visit = obj.event_set.filter(
                        tipus=Event.EventType.GOL,
                                equip=obj.visitant).count()
        return "{} - {}".format(gols_local,gols_visit)

admin.site.register(Partit,PartitAdmin)

class EventAdmin(admin.ModelAdmin):
    list_display = ["partit","temps","tipus","equip","jugador"]
    ordering = ("-temps",)

admin.site.register(Event,EventAdmin)

