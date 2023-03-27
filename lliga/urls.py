from django.urls import path

from lliga import views


urlpatterns = [
    path('menu', views.menu),
    path('taula_partits', views.taula_partits ),
    path('classificacio', views.classificacio2 ),
    path('classificacio/<int:lliga_id>', views.classificacio2, name="classificacio"),
]
