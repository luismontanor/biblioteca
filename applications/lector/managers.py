import datetime
from itertools import count

from unittest import result
from django.db import models

from django.db.models import Q, Count, Avg, Sum
from django.db.models.functions import Lower

class PrestamoManager(models.Manager):
    """Manager para el modelo Prestamo"""

    # Filtro para calcular el promedio de edades de las personas que han hecho prestamo de un determinado libro
    def libros_promedio_edades(self):
        # Para el procedimiento primero tenemos que filtrar para obtener el libro del que deseamos obtener el promedio de edades de los lectores
        resultado = self.filter(
            libro__id='6',
        ).aggregate(
            # Con esta operacion se procede a calcular el promedio de edades de los lectores
            promedio_edad = Avg('lector__edad'),
            suma_edad = Sum('lector__edad')
        )
        return resultado

    # Consulta para determinar la cantidad de veces que se ha prestado un libro
    def num_libros_prestados(self):
        resultado = self.values(
            'libro'
        ).annotate(
            num_prestamos = Count('libro'),
            # Se utiliza esta funcion para agregar el titulo del libro al array de diccionarios que devueve la funcion
            titulo = Lower('libro__titulo'),
        )

        for r in resultado:
            print('*****************')
            print(r, r['num_prestamos'])
        return resultado
