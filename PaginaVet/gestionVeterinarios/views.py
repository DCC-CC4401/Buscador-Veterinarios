from django.shortcuts import render, redirect
from django.http import HttpResponse
import datetime
from django.template import Template, Context
from django.template.loader import get_template
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

def perfil(request):

    return render(request, "gestionVeterinarios/base.html", {})