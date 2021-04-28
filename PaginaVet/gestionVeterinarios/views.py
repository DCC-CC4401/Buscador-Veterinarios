from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponse
import datetime
from django.template import Template, Context
from django.template.loader import get_template
from django.db import connection
# Create your views here.
from gestionVeterinarios.models import Veterinario, Reseña, User

def index(request):
    return render(request, "gestionVeterinarios/index.html")

def registroUsuario(request):
    return render(request, "gestionVeterinarios/registroUsuario.html")


def formVeterinario(request): #the index view
    if request.method == "GET":
        return render(request, "gestionVeterinarios/formVeterinario.html")

    elif request.method == "POST":
        nombre = request.POST["nombre"]
        apellidos = request.POST["apellidos"]
        pronombre = request.POST["pronombre"]
        descripcion = request.POST["descripcion"]
        foto = request.FILES.get("foto")
        nombre_consulta= request.POST["nombre_consulta"]
        region = request.POST["region"]
        comuna = request.POST["comuna"]
        especialidad = request.POST["especialidad"]
        animales_lista = request.POST.getlist("animales")
        animales = ' '.join(animales_lista)
        if request.POST["visitas_a_domicilio"] == "si":
            visitas_a_domicilio = True
        else:
            visitas_a_domicilio = False
        if request.POST["urgencias"] == "si":
            urgencias = True
        else:
            urgencias = False
        horario_atencion_lista = request.POST.getlist("horario_atencion")
        horario_atencion = ' '.join(horario_atencion_lista)
        telefono = request.POST["telefono"]
        email = request.POST["email"]
        pagina_web = request.POST["pagina_web"]

        nuevo_veterinario = Veterinario(nombre=nombre, apellido=apellidos, pronombre=pronombre,
         descripcion = descripcion,foto=foto, nombre_consulta=nombre_consulta, region=region, comuna=comuna,
          especialidad=especialidad, animales=animales, visitas_a_domicilio=visitas_a_domicilio,urgencias=urgencias,
           horario_atencion=horario_atencion, telefono=telefono, email=email, pagina_web=pagina_web)
        nuevo_veterinario.save()

        return redirect('/confirmacionRegistroVet')

def confirmacionRegistroVet(request):
    if request.method == "GET":
        return render(request, "gestionVeterinarios/confirmacionRegistroVet.html")

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

        return redirect("/confirmacionEvaluacion")

def confirmacionEvaluacion(request):
    if request.method == "GET":
        return render(request, "gestionVeterinarios/confirmacionEvaluacion.html")

def catalogoVeterinarios(request):
    if request.method == "GET":
        doctores=Veterinario.objects.all()
        evaluaciones=Reseña.objects.all()

        return render(request, "gestionVeterinarios/catalogodoc.html", {"doctores":doctores, "evaluaciones":evaluaciones})

def perfil(request, id_vet):

    if request.method == "GET":
        doctor=Veterinario.objects.get(id=id_vet)
        return render(request, "gestionVeterinarios/perfildoc.html", {"doctor":doctor})