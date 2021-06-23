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
        especialidad_lista = request.POST.getlist("especialidad")
        especialidad = ';'.join(especialidad_lista)
        animales_lista = request.POST.getlist("animales")
        animales = ';'.join(animales_lista)
        if request.POST["visitas_a_domicilio"] == "si":
            visitas_a_domicilio = True
        else:
            visitas_a_domicilio = False
        if request.POST["urgencias"] == "si":
            urgencias = True
        else:
            urgencias = False
        horario_atencion_lista = request.POST.getlist("horario_atencion")
        horario_atencion = ';'.join(horario_atencion_lista)
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

def catalogoVeterinarios(request, f):

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

    filtros = {}

    especie = request.GET.get("especie")
    especialidad = request.GET.get("especialidad")
    region = request.GET.get("region")
    comuna = request.GET.get("comuna")
    domicilio = request.GET.get("domicilio")
    urgencia = request.GET.get("urgencia")
    busqueda = request.GET.get("buscar")

    if f == '0' or especie or especialidad or region or comuna or domicilio or urgencia or busqueda:

        if request.method == "GET":

            print(especie)
            print(especialidad)
            print(region)
            print(comuna)
            print(domicilio)
            print(urgencia)

            if especie or especialidad or region or comuna or domicilio or urgencia:
                insert = ''''''
                
                if especie == 'Any':
                    especie = None

                if especialidad == 'Any':
                    especialidad = None

                if especie:
                    insert += ''' AND v.animales LIKE "%''' + especie + '''%"'''
                    filtros['especie'] = especie
                if especialidad:
                    insert += ''' AND v.especialidad LIKE "%''' + especialidad + '''%"'''
                    filtros['especialidad'] = especialidad
                if region:
                    insert +=  ''' AND v.region LIKE "''' + region + '''"'''
                    filtros['region'] = region
                if comuna:
                    insert += ''' AND v.comuna LIKE "''' + comuna + '''"'''
                    filtros['comuna'] = comuna
                if domicilio == "si":
                    insert += ''' AND v.visitas_a_domicilio = True'''
                    filtros['domicilio'] = domicilio
                if urgencia == "si":
                    insert += ''' AND v.urgencias = True'''
                    filtros['urgencia'] = urgencia

                veterinarios = Veterinario.objects.raw('''
                SELECT v.id, v.nombre, v.apellido, v.region, v.comuna, v.urgencias, v.visitas_a_domicilio, AVG(r.evaluacion) as prom_evaluacion
                FROM gestionVeterinarios_veterinario v, gestionVeterinarios_reseña r
                WHERE v.id = r.id_veterinario_id''' + insert + ''' GROUP BY v.id
                ''')
                veterinarios_sin_eval = Veterinario.objects.raw('''
                SELECT v.id, v.nombre, v.apellido, v.region, v.comuna, v.urgencias, v.visitas_a_domicilio
                FROM gestionVeterinarios_veterinario v
                WHERE v.id NOT in 
                (SELECT r.id_veterinario_id
                FROM gestionVeterinarios_reseña r)''' + insert)
            
            print(busqueda)
            if busqueda:
                filtros['busqueda'] = busqueda
                veterinarios = Veterinario.objects.raw('''
                SELECT id, Q.nombre, Q.apellido, Q.region, Q.comuna, Q.urgencias, Q.visitas_a_domicilio, Q.prom_evaluacion
                FROM (
                SELECT v.id, v.nombre, v.apellido, v.region, v.comuna, v.urgencias, v.visitas_a_domicilio, AVG(r.evaluacion) as prom_evaluacion,
                v.nombre || ' ' || v.apellido as nc
                FROM gestionVeterinarios_veterinario v, gestionVeterinarios_reseña r
                WHERE v.id = r.id_veterinario_id
                GROUP BY v.id) as Q
                WHERE Q.nc LIKE "%'''+ busqueda +'''%"
                ''')
                veterinarios_sin_eval = Veterinario.objects.raw('''
                SELECT id, Q.nombre, Q.apellido, Q.region, Q.comuna, Q.urgencias, Q.visitas_a_domicilio
                FROM (
                SELECT v.id, v.nombre, v.apellido, v.region, v.comuna, v.urgencias, v.visitas_a_domicilio, 
                v.nombre || ' ' || v.apellido AS nc
                FROM gestionVeterinarios_veterinario v
                WHERE v.id NOT in 
                (SELECT r.id_veterinario_id
                FROM gestionVeterinarios_reseña r)) as Q
                WHERE Q.nc LIKE "%'''+ busqueda +'''%"
                ''')

        return render(request, "gestionVeterinarios/catalogodoc.html", {"veterinarios":veterinarios, "veterinarios_sin_eval": veterinarios_sin_eval, "reg":reg, "filtros":filtros})
    
    else:
        f = '0'
        return render(request, "gestionVeterinarios/formBusqueda.html", {"veterinarios":veterinarios, "veterinarios_sin_eval": veterinarios_sin_eval, "reg":reg, "filtros":filtros})


def perfil(request, id_vet):

    if request.method == "GET":
        veterinario=Veterinario.objects.get(id=id_vet)
        region = reg[veterinario.region]
        horario = veterinario.horario_atencion
        dias = horario.split(';')
        stringAnimales = veterinario.animales
        animales = stringAnimales.split(';')
        stringEspecialidades = veterinario.especialidad
        especialidades = stringEspecialidades.split(';')
        evaluaciones = Reseña.objects.filter(id_veterinario_id=id_vet)
        prom_evaluacion = Reseña.objects.raw('''
        SELECT id, AVG(evaluacion) as prom
        FROM gestionVeterinarios_reseña
        WHERE id_veterinario_id = %s
        ''' % id_vet)
        if request.user.is_authenticated:
            user_vet_id = int(request.user.veterinario.id)
            return render(request, "gestionVeterinarios/perfildoc.html", {"veterinario":veterinario, "evaluaciones":evaluaciones, "prom_evaluacion": prom_evaluacion, "dias": dias, "animales":animales, "region":region, "especialidades": especialidades, "user_vet_id": user_vet_id})
        else:
            return render(request, "gestionVeterinarios/perfildoc.html", {"veterinario":veterinario, "evaluaciones":evaluaciones, "prom_evaluacion": prom_evaluacion, "dias": dias, "animales":animales, "region":region, "especialidades": especialidades, "user_vet_id": None})

def editarPerfil(request):

    if request.method == "GET":
        if request.user.is_authenticated:
            veterinario = request.user.veterinario
            region = reg[veterinario.region]
            horario = veterinario.horario_atencion
            dias = horario.split(';')
            stringAnimales = veterinario.animales
            animales = stringAnimales.split(';')
            evaluaciones = Reseña.objects.filter(id_veterinario_id=veterinario.id)
            prom_evaluacion = Reseña.objects.raw('''
            SELECT id, AVG(evaluacion) as prom
            FROM gestionVeterinarios_reseña
            WHERE id_veterinario_id = %s
            ''' % veterinario.id)
            return render(request, "gestionVeterinarios/editarPerfil.html", {"veterinario":veterinario, "evaluaciones":evaluaciones, "prom_evaluacion": prom_evaluacion, "dias": dias, "animales":animales, "region":region})     
        else:
            return HttpResponseRedirect('../ingresoVeterinarios')
        
    elif request.method == "POST":
        user_vet = request.user.veterinario
        user_vet.nombre = request.POST["nombre"]
        user_vet.apellido = request.POST["apellidos"]
        user_vet.pronombre = request.POST["pronombre"]
        user_vet.descripcion = request.POST["descripcion"]
        if request.FILES.get("foto"):
            user_vet.foto = request.FILES.get("foto")
        user_vet.nombre_consulta= request.POST["nombre_consulta"]
        user_vet.region = request.POST["region"]
        user_vet.comuna = request.POST["comuna"]
        especialidad_lista = request.POST.getlist("especialidad")
        user_vet.especialidad = ';'.join(especialidad_lista)
        animales_lista = request.POST.getlist("animales")
        user_vet.animales = ';'.join(animales_lista)
        if request.POST["visitas_a_domicilio"] == "si":
            user_vet.visitas_a_domicilio = True
        else:
            user_vet.visitas_a_domicilio = False
        if request.POST["urgencias"] == "si":
            user_vet.urgencias = True
        else:
            user_vet.urgencias = False
        horario_atencion_lista = request.POST.getlist("horario_atencion")
        user_vet.horario_atencion = ';'.join(horario_atencion_lista)
        if request.POST["telefono"]=="":
            user_vet.telefono=None
        else:
            user_vet.telefono = request.POST["telefono"]

        user_vet.pagina_web = request.POST["pagina_web"]
        user_vet.save()
        
        return redirect('/perfil/'+str(user_vet.id))
