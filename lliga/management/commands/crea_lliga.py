from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from faker import Faker
from datetime import timedelta, time
from random import randint

from lliga.models import *

faker = Faker(["es_CA","es_ES"])

class Command(BaseCommand):
    help = 'Crea una lliga amb equips i jugadors'

    def add_arguments(self, parser):
        parser.add_argument('titol_lliga', nargs=1, type=str)

    def handle(self, *args, **options):
        titol_lliga = options['titol_lliga'][0]
        lliga = Lliga.objects.filter(titol=titol_lliga)
        if lliga.count()>0:
            print("Aquesta lliga ja està creada. Posa un altre nom.")
            return

        print("Creem la nova lliga: {}".format(titol_lliga))
        lliga = Lliga(  titol=titol_lliga,
                        inici=timezone.now(),
                        final=timezone.now()+timedelta(days=11*30))
        lliga.save()

        print("Creem equips")
        prefixos = ["RCD", "Athletic", "", "Deportivo", "Unión Deportiva"]
        for i in range(20):
            ciutat = faker.city()
            prefix = prefixos[randint(0,len(prefixos)-1)]
            if prefix:
                prefix += " "
            nom =  prefix + ciutat
            equip = Equip(ciutat=ciutat,nom=nom)
            #print(equip)
            equip.save()
            lliga.equips.add(equip)

            print("Creem jugadors de l'equip "+nom)
            for i in range(25):
                nom = faker.first_name()
                cognom1 = faker.last_name()
                cognom2 = faker.last_name()
                jugador = Jugador(nom=nom,cognom1=cognom1,cognom2=cognom2,alias=nom+" "+cognom1)
                #print(jugador)
                jugador.save()
                fitxa = Fitxa(jugador=jugador,equip=equip,inici=timezone.now(),dorsal=i+1)
                fitxa.save()

        print("Creem partits de la lliga")
        for local in lliga.equips.all():
            for visitant in lliga.equips.all():
                if local!=visitant:
                    partit = Partit(local=local,visitant=visitant)
                    partit.local = local
                    partit.visitant = visitant
                    partit.lliga = lliga
                    partit.save()
                    # crea gols (events)
                    for i in range(randint(0,6)):
                        loc_or_visit = randint(0,1)
                        numjug = randint(0,20)
                        if loc_or_visit:
                            gol = Event(
                                tipus=Event.EventType.GOL,
                                partit=partit,
                                temps=time(0,randint(0,59),randint(0,59)),
                                equip=local,
                                jugador=local.fitxa_set.all()[numjug].jugador,
                                )
                            gol.save()
                        else:
                            gol = Event(
                                tipus=Event.EventType.GOL,
                                partit=partit,
                                temps=time(0,randint(0,59),randint(0,59)),
                                equip=visitant,
                                jugador=local.fitxa_set.all()[numjug].jugador,
                                )
                            gol.save()
