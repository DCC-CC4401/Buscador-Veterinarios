from django.db import models
from django.contrib.auth.models import AbstractUser
#from django.contrib.postgres.fields import ArrayField

# Aca va una clase por cada tabla de la Base de Datos

# User de django 
class User(AbstractUser):
    # Ya viene con username, contraseña y email
    Apodo = models.CharField(max_length=30)
# Datos de veterinarios
class Veterinario(models.Model):
    pronombres = [('Dr', 'Dr.'), ('Dra','Dra.')]
    # Datos personales
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=60)
    pronombre = models.CharField(max_length=5,choices=pronombres)
    descripcion = models.CharField(max_length=500)
    foto = models.ImageField()

    # Datos de trabajo
    tipos_animales = [('Domesticos', 'Domesticos'), ('Equinos', 'Equinos'), ('Ganado', 'Ganado'), ('Exoticos', 'Exóticos')]
    nombre_consulta = models.CharField(max_length=80)
    region = models.CharField()
    comuna = models.CharField()
    especialidad = models.CharField()
    animales = models.CharField(choices=pronombres)
    visitas_a_domicilio = models.BooleanField()
    urgencias = models.BooleanField()

    # Datos de contacto de veterinarios
    horario_atencion = models.CharField()
    #horario_atencion = ArrayField(models.CharField(max_length=100), blank=True)
    telefono = models.IntegerField()
    email = models.EmailField()
    pagina_web = models.CharField()

class Reseña(models.Model):
    nombre = models.CharField(max_length=30)
    evaluacion = models.FloatField()
    problema_resuelto = models.BooleanField()
    razon_consulta = models.CharField(50)
    comentario = models.CharField()


