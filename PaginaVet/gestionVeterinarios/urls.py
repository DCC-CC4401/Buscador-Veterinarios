from django.urls import path # type: ignore
from . import views
urlpatterns = [
  path('ingresoVeterinarios', views.formVeterinario),
  path('confirmacionRegistroVet/', views.confirmacionRegistroVet),
  path('evaluacionVeterinarios/<id_vet>/', views.formEvaluacion, name="eval_vet"),
  path('catalogoVeterinarios/<f>/', views.catalogoVeterinarios, name="catalogo_vet"),
  path('perfil/<id_vet>/', views.perfil, name="perfil_vet"),
  path('confirmacionEvaluacion/', views.confirmacionEvaluacion),
  path('login/', views.login_user),
  path('logout/', views.logout_user),
  path('', views.index),
  path('editarperfil', views.editarPerfil, name="edit_vet"),
]       