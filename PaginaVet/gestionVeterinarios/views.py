from django.shortcuts import render, redirect
from django.http import HttpResponse
import datetime
from django.template import Template, Context
from django.template.loader import get_template
# Create your views here.
from gestionVeterinarios.models import Veterinario, Reseña, User

def index(request):
    return render(request, "gestionVeterinarios/index.html")

def formVeterinario(request): #the index view
   if request.method == "GET":
       return render(request, "gestionVeterinarios/formVeterinario.html")


def formEvaluacion(request):
    if request.method == "GET":
        return render(request, "gestionVeterinarios/formevaluacion.html")
    elif request.method == "POST":
        nombre=request.POST["nombre"]
        if request.POST["estrellas"] == "5":
            estrellas = 5
        elif request.POST["estrellas"] == "4":
            estrellas = 4
        elif request.POST["estrellas"] == "3":
            estrellas = 3
        elif request.POST["estrellas"] == "2":
            estrellas = 2
        else:
            estrellas = 1
        razon_consulta=request.POST["razon_consulta"]       
        if request.POST["problema_resuelto"] == "si":
            problema_resuelto = True
        else:
            problema_resuelto = False

        comentario=request.POST["comentario"]

        nueva_resena = Reseña(nombre=nombre, evaluacion=estrellas, problema_resuelto=problema_resuelto, razon_consulta=razon_consulta,comentario=comentario)
        nueva_resena.save()

        return redirect("/evaluacionVeterinarios")



def catalogoVeterinarios(request):
    if request.method == "GET":
        doctores=Veterinario.objects.all()
        return render(request, "gestionVeterinarios/catalogodoc.html", {"doctores":doctores})

def perfil(request):

    return render(request, "gestionVeterinarios/perfildoc.html", {})