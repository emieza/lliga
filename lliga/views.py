from django.shortcuts import render
from django import forms
from django.shortcuts import redirect

from lliga.models import *

# Create your views here.

class TriaLligaForm(forms.Form):
    lliga = forms.ModelChoiceField(queryset=Lliga.objects.all())

def menu(request):
    form = TriaLligaForm()
    if request.method == "POST":
        form = TriaLligaForm(request.POST)
        if form.is_valid():
            lliga = form.cleaned_data.get("lliga")
            return redirect('classificacio',lliga.id)
    return render(request, "menu.html",{
                    "form": form,
            })

def classificacio(request,lliga_id=None):
    lliga = Lliga.objects.first()
    if lliga_id:
        lliga = Lliga.objects.get(pk=lliga_id)
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
                    "lliga":lliga,
                    "classificacio":classi,
                })

# optimització
def classificacio2(request,lliga_id=None):
    lliga = Lliga.objects.first()
    if lliga_id:
        lliga = Lliga.objects.get(pk=lliga_id)
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
                    "lliga":lliga,
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


class LligaForm(forms.ModelForm):
    class Meta:
        model = Lliga
        exclude = []

def crea_lliga(request):
    form = LligaForm()
    message = ""
    if request.method == "POST":
        form = LligaForm(request.POST)
        if form.is_valid():
            titol = form.cleaned_data.get("titol")
            lliga2 = Lliga.objects.filter(titol=titol)
            if lliga2.count() > 0:
                message = "El nom de la lliga ja existeix, posa'n un altre"
            else:
                form.save()
                message = "Lliga '{}' guardada".format(titol)
                form = LligaForm()
    return render(  request, "crea_lliga.html",
                    {"form":form,"message":message})

class PartitForm(forms.Form):
    local = forms.ModelChoiceField(queryset=Equip.objects.all())
    visitant = forms.ModelChoiceField(queryset=Equip.objects.all())

def crea_partit(request,lliga_id=None):
    message = ""
    if not lliga_id:
        if request.method=="GET":
            # PAS 1: triar lliga
            form = TriaLligaForm()
            return render(request,"crea_partit.html",{"form":form})
        else:
            # PAS 2: anar a seleccionar equips
            form = TriaLligaForm(request.POST)
            if form.is_valid():
                lliga = form.cleaned_data.get("lliga")
                return redirect("crea_partit2",lliga.id)
    # PAS 3: triar equips del partit
    if request.method=="GET":
        form = PartitForm()
        return render(request,"crea_partit.html",{"form":form})
    else:
        form = PartitForm(request.POST)
        if form.is_valid():
            message = "Funció encara no implementada"
        return render(request,"crea_partit.html",{"form":form,"message":message})



def edita_partit(request,partit_id=None):
    return render(request,"not_implemented.html")


def edita_partit_advanced(request):
    message = ""
    partit = None
    if request.method=="POST":
        lliga_id = request.POST.get("lliga")
        local_id = request.POST.get("local")
        visitant_id = request.POST.get("visitant")
        if local_id == visitant_id:
            message = "Has seleccionat el mateix equip 2 cops."
        else:
            partit = Partit.objects.filter(local__id=local_id,visitant__id=visitant_id)
            if partit:
                message = "El partit ja existeix. Inicia l'edició."
                partit = partit.get()
            else:
                lliga = Lliga.objects.get(pk=lliga_id)
                local = Equip.objects.get(pk=local_id)
                visitant = Equip.objects.get(pk=visitant_id)
                partit = Partit(lliga=lliga,local=local,visitant=visitant)
                partit.save()
                message = "Partit creat correctament"
    return render(request,"edita_partit_advanced.html",{"message":message,"partit":partit})

