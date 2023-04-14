from django.contrib import admin
from django.urls import include,path

from lliga import api

urlpatterns = [
    path('get_lligues', api.get_lligues ),
    path('get_equips/<int:lliga_id>', api.get_equips ),
]
