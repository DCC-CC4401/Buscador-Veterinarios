from django.shortcuts import render, redirect, HttpResponseRedirect # type: ignore
from django.http import HttpResponse # type: ignore
import datetime
from django.template import Template, Context # type: ignore
from django.template.loader import get_template # type: ignore
from django.db import connection # type: ignore
from django.contrib.auth import authenticate, login,logout # type: ignore
from django.db.models import Q # type: ignore
# Create your views here.
from gestionVeterinarios.models import Veterinario, Reseña, User # type: ignore

def index(request):
    return render(request, "gestionVeterinarios/index.html")

def login_user(request):
    if request.method == 'GET':
        return render(request, "gestionVeterinarios/login.html")
    if request.method == 'POST':
        username = request.POST['username']
        contraseña = request.POST['contraseña']
        usuario = authenticate(username=username, password=contraseña)

        if usuario is not None:
            login(request,usuario)
            return redirect(perfil, id_vet=usuario.veterinario.id)
        else:
            return HttpResponseRedirect('../ingresoVeterinarios')

def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')

def formVeterinario(request): #the index view
    if request.method == "GET":
        return render(request, "gestionVeterinarios/formVeterinario.html")

    elif request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        repeat_password = request.POST["repeat_password"]

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
        if request.POST["telefono"]=="":
            telefono=None
        else:
            telefono = request.POST["telefono"]

        pagina_web = request.POST["pagina_web"]

        if repeat_password == password:
            nuevo_veterinario = Veterinario(nombre=nombre, apellido=apellidos, pronombre=pronombre,
            descripcion = descripcion,foto=foto, nombre_consulta=nombre_consulta, region=region, comuna=comuna,
            especialidad=especialidad, animales=animales, visitas_a_domicilio=visitas_a_domicilio,urgencias=urgencias,
            horario_atencion=horario_atencion, telefono=telefono, email=email, pagina_web=pagina_web)

            nuevo_veterinario.save()
            nuevo_user = User.objects.create_user(username=username, password=password, email=email, veterinario=nuevo_veterinario)
            return redirect('/confirmacionRegistroVet')
        else:
            return redirect('/ingresoVeterinarios')

def confirmacionRegistroVet(request):
    if request.method == "GET":
        return render(request, "gestionVeterinarios/confirmacionRegistroVet.html")



def formEvaluacion(request, id_vet):
    veterinario=Veterinario.objects.get(id=id_vet)
    if request.method == "GET":
        return render(request, "gestionVeterinarios/formevaluacion.html", {"veterinario":veterinario})
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

        nueva_resena = Reseña(id_veterinario=veterinario, nombre=nombre, evaluacion=estrellas, problema_resuelto=problema_resuelto, razon_consulta=razon_consulta,comentario=comentario)
        nueva_resena.save()

        return redirect("/confirmacionEvaluacion")

def confirmacionEvaluacion(request):
    if request.method == "GET":
        return render(request, "gestionVeterinarios/confirmacionEvaluacion.html")

reg = {
    "XV": "Arica y Parinacota",
    "I": "Tarapacá",
    "II": "Antofagasta",
    "III": "Atacama",
    "IV": "Coquimbo",
    "V": "Valparaíso",
    "RM": "Metropolitana de Santiago",
    "VI": "Libertador Gral. Bernardo O’Higgins",
    "VII": "Maule",
    "XVI": "Ñuble",
    "VIII": "Biobío",
    "IX": "Araucanía",
    "XIV": "Los Ríos",
    "X": "Los Lagos",
    "XI": "Aisén del Gral. Carlos Ibáñez del Campo",
    "XII": "Magallanes y de la Antártica Chilena"
}

def catalogoVeterinarios(request):
    if request.method == "GET":
        veterinarios = Veterinario.objects.raw('''
        SELECT v.id, v.nombre, v.apellido, v.region, v.comuna, v.urgencias, v.visitas_a_domicilio, AVG(r.evaluacion) as prom_evaluacion
        FROM gestionVeterinarios_veterinario v, gestionVeterinarios_reseña r
        WHERE v.id = r.id_veterinario_id
        GROUP BY v.id
        ''')
        veterinarios_sin_eval = Veterinario.objects.raw('''
        SELECT v.id, v.nombre, v.apellido, v.region, v.comuna, v.urgencias, v.visitas_a_domicilio
        FROM gestionVeterinarios_veterinario v
        WHERE v.id NOT in 
        (SELECT r.id_veterinario_id
        FROM gestionVeterinarios_reseña r)
        ''')

        busqueda = request.GET.get("buscar")
        print(busqueda)
        if busqueda:
            veterinarios = Veterinario.objects.raw('''
            SELECT v.id, v.nombre, v.apellido, v.region, v.comuna, v.urgencias, v.visitas_a_domicilio, AVG(r.evaluacion) as prom_evaluacion
            FROM gestionVeterinarios_veterinario v, gestionVeterinarios_reseña r
            WHERE v.id = r.id_veterinario_id
            AND v.nombre LIKE '%s'
            GROUP BY v.id
            ''' % busqueda)
            veterinarios_sin_eval = Veterinario.objects.raw('''
            SELECT v.id, v.nombre, v.apellido, v.region, v.comuna, v.urgencias, v.visitas_a_domicilio
            FROM gestionVeterinarios_veterinario v
            WHERE v.id NOT in 
            (SELECT r.id_veterinario_id
            FROM gestionVeterinarios_reseña r)
            AND v.nombre LIKE '%s'
            ''' % busqueda)


        return render(request, "gestionVeterinarios/catalogodoc.html", {"veterinarios":veterinarios, "veterinarios_sin_eval": veterinarios_sin_eval, "reg":reg})

def perfil(request, id_vet):

    if request.method == "GET":
        veterinario=Veterinario.objects.get(id=id_vet)
        region = reg[veterinario.region]
        horario = veterinario.horario_atencion
        dias = horario.split(' ')
        stringAnimales = veterinario.animales
        animales = stringAnimales.split(' ')
        evaluaciones = Reseña.objects.filter(id_veterinario_id=id_vet)
        prom_evaluacion = Reseña.objects.raw('''
        SELECT id, AVG(evaluacion) as prom
        FROM gestionVeterinarios_reseña
        WHERE id_veterinario_id = %s
        ''' % id_vet)
        return render(request, "gestionVeterinarios/perfildoc.html", {"veterinario":veterinario, "evaluaciones":evaluaciones, "prom_evaluacion": prom_evaluacion, "dias": dias, "animales":animales, "region":region})