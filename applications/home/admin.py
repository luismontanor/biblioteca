from django.contrib import admin
from .models import Empleados, Persona

admin.site.register(Persona)
admin.site.register(Empleados)