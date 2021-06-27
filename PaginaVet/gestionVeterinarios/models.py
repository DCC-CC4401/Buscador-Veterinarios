from django.db import models # type: ignore
from django.contrib.auth.models import AbstractUser # type: ignore
#from django.contrib.postgres.fields import ArrayField

# Aca va una clase por cada tabla de la Base de Datos

# Datos de veterinarios
class Veterinario(models.Model):
    pronombres_posibles = [('Dr.', 'Dr.'), ('Dra.','Dra.')]
    # Datos personales
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=60)
    pronombre = models.CharField(max_length=5,choices=pronombres_posibles)
    descripcion = models.CharField(max_length=500, blank=True)
    foto = models.ImageField(upload_to='fotos', blank=True, null=True)

    # Datos de trabajo
    nombre_consulta = models.CharField(max_length=80, blank=True)
    region = models.CharField(max_length=80)
    comuna = models.CharField(max_length=80)
    especialidad = models.CharField(max_length=80)
    animales = models.CharField(max_length=80)
    visitas_a_domicilio = models.BooleanField()
    urgencias = models.BooleanField()

    # Datos de contacto de veterinarios
    horario_atencion = models.CharField(max_length=300)
    telefono = models.IntegerField(blank=True, null=True)
    email = models.EmailField()
    pagina_web = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return (self.nombre + self.apellido)

class Reseña(models.Model):
    id_veterinario = models.ForeignKey(Veterinario, related_name='Veterinario', on_delete=models.CASCADE, null=True)
    nombre = models.CharField(max_length=30)
    evaluacion = models.FloatField()
    problema_resuelto = models.BooleanField()
    razon_consulta = models.CharField(max_length=50)
    comentario = models.CharField(max_length=600, blank=True)

    def __str__(self):
        return (self.nombre)

# User de django 
class User(AbstractUser):
    # Ya viene con username, first_name, last_name, contraseña y email
    veterinario = models.OneToOneField(Veterinario, on_delete=models.CASCADE, default=None, null=True, blank=True)

