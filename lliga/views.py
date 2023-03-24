from django.shortcuts import render

from lliga.models import *

# Create your views here.

def classificacio(request):
	lliga = Lliga.objects.first()
	return render(request,"classificacio.html",
					{"lliga":lliga})


def taula_partits(request):
	lliga = Lliga.objects.first()
	return render(request,"taula_partits.html",
					{"lliga":lliga})


