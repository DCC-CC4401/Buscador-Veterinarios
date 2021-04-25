from django.urls import path
from . import views

urlpatterns = [
  path('ingresoVeterinarios', views.formVeterinario),
  path('evaluacionVeterinarios', views.formEvaluacion),
  path('catalogoVeterinarios', views.catalogoVeterinarios),
  path('perfil/', views.perfil),
]     