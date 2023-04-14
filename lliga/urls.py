from django.urls import path

from lliga import views


urlpatterns = [
    path('menu', views.menu),
    path('taula_partits', views.taula_partits ),
    path('classificacio', views.classificacio2 ),
    path('classificacio/<int:lliga_id>', views.classificacio2, name="classificacio"),
    path('crea_lliga', views.crea_lliga ),
    path('crea_partit', views.crea_partit, name="crea_partit" ),
    path('crea_partit/<int:lliga_id>', views.crea_partit, name="crea_partit2" ),
    path('edita_partit/<int:partit_id>', views.edita_partit ),
    path('edita_partit_advanced/', views.edita_partit_advanced ),
]
