from django.urls import path

from lliga import views


urlpatterns = [
    path('taula_partits', views.taula_partits),
    path('classificacio', views.classificacio),
]
