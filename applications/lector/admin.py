from django.contrib import admin

from .models import Lector, Prestamo

# Register your models here.
admin.site.register(Prestamo)
admin.site.register(Lector)