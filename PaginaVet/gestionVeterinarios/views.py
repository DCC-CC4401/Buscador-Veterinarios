from django.shortcuts import render, redirect

# Create your views here.
from gestionVeterinarios.models import Veterinario, Reseña, User


def formVeterinario(request): #the index view
   if request.method == "GET":
       return render(request, "gestionVeterinarios/formVeterinario.html")


def formEvaluacion(request):
    if request.method == "GET":
        return render(request, "gestionVeterinarios/formevaluacion.html")

def catalogoVeterinarios(request):
    if request.method == "GET":
        return render(request, "gestionVeterinarios/catalogodoc.html")