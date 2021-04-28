from django.urls import path
from . import views

urlpatterns = [
  path('ingresoVeterinarios', views.formVeterinario),
  path('confirmacionRegistroVet/', views.confirmacionRegistroVet),
  path('evaluacionVeterinarios', views.formEvaluacion),
  path('catalogoVeterinarios', views.catalogoVeterinarios),
  path('perfil/<id_vet>/', views.perfil, name="perfil_vet"),
  path('', views.index),
]     