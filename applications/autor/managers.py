from unittest import result
from django.db import models

from django.db.models import Q

class AutorManager(models.Manager):
    """Manager para el modelo Autor"""

    # Consultar valores de coincidencia en los nombres
    def buscar_autor(self, kword):
        resultado = self.filter(
            nombres__icontains=kword
            )

        return resultado

    # Consultar valores de coincidencias en los nombres y apellidos
    def buscar_autor2(self, kword):
        resultado = self.filter(
            Q(nombres__icontains=kword) | Q(apellidos__icontains=kword)
            )

        return resultado

    # Consultar valores de coincidencia dentro de un campo excluyendo determinados valores
    def buscar_autor3(self, kword):
        resultado = self.filter(
            nombres__icontains=kword
            ).exclude(
                 Q(edad__icontains=65) | Q(edad__icontains=68)
                )

        return resultado

    # Consultar los registros cuyos valores de edad esten dentro de un rango determinado
    def buscar_autor4(self, kword):
        resultado = self.filter(
            # De esta forma se expresa mayor que
            edad__gt=50,
            # De esta forma se expresa mayor que
            edad__lt=70,
            ).order_by('apellidos', 'nombres', 'id')

        return resultado