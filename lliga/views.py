from django.shortcuts import render

from lliga.models import *

# Create your views here.

def classificacio(request):
    lliga = Lliga.objects.first()
    equips = lliga.equips.all()
    classi = []

    # calculem punts en llista de tuples (equip,punts)
    for equip in equips:
        punts = 0
        for partit in lliga.partit_set.filter(local=equip):
            if partit.gols_local() > partit.gols_visitant():
                punts += 3
            elif partit.gols_local() == partit.gols_visitant():
                punts += 1
        for partit in lliga.partit_set.filter(visitant=equip):
            if partit.gols_local() < partit.gols_visitant():
                punts += 3
            elif partit.gols_local() == partit.gols_visitant():
                punts += 1
        classi.append( (punts,equip.nom) )
    # ordenem llista
    classi.sort(reverse=True)
    return render(request,"classificacio.html",
                {
                    "classificacio":classi,
                })

# optimització
def classificacio2(request):
    lliga = Lliga.objects.first()
    equips = lliga.equips.all()
    punts = {}
    for equip in equips:
        punts[equip.nom] = 0
    # calculem punts en llista de tuples (equip,punts)
    for partit in lliga.partit_set.all():
        if partit.gols_local() > partit.gols_visitant():
            punts[partit.local.nom] += 3
        elif partit.gols_local() == partit.gols_visitant():
            punts[partit.local.nom] += 1
            punts[partit.visitant.nom] += 1
        else:
            punts[partit.visitant.nom] += 3
    # ordenem llista
    classi = []
    for equip in equips:
        classi.append( (punts[equip.nom], equip.nom) )
    classi.sort(reverse=True)
    return render(request,"classificacio.html",
                {
                    "classificacio":classi,
                })



def taula_partits(request):
    # per mostrar la taula de partits, creem una matriu (resultats)
    # per renderitzar-la després de forma senzilla a la view
    lliga = Lliga.objects.first()
    equips = [ equip.nom for equip in lliga.equips.order_by("nom") ]
    resultats = []
    resultats.append( [""] + equips )
    for local in equips:
        local_res = [local,]
        for visitant in equips:
            if local!=visitant:
                partit = lliga.partit_set.filter(local__nom=local,visitant__nom=visitant)
                if not partit:
                    local_res.append("")
                else:
                    local_res.append(str(partit.get().gols_local())+"-"+str(partit.get().gols_visitant()))
            else:
                local_res.append("x")
        resultats.append(local_res)

    # renderitzem una taula genèrica, trobat a:
    # https://stackoverflow.com/questions/17410058/django-how-to-render-a-matrix
    return render(request,"taula_partits.html",
                {
                    "lliga":lliga,
                    "equips":equips,
                    "resultats": resultats,
                })


