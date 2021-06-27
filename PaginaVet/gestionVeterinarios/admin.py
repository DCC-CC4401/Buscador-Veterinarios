from django.contrib import admin # type: ignore
from gestionVeterinarios.models import Veterinario, User, Reseña # type: ignore

admin.site.register(Veterinario)
admin.site.register(User)
admin.site.register(Reseña)