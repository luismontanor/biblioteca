import datetime
from django.db import models
from django.db.models import Q, Count
from django.contrib.postgres.search import TrigramSimilarity


class LibroManager(models.Manager):
    """Manager para el modelo Libro"""
    # Consultar valores de coincidencia en un rango de fecha
    def listar_libros(self, kword):
        resultado = self.filter(
            titulo__icontains=kword,
            fecha__range=('2000-01-01', '2021-10-01'),
            )
        return resultado

    # Funcion de busqueda con el trigram de postgresql
    def listar_libros_trg(self, kword):

        if(kword):
            resultado = self.filter(
                titulo__trigram_similar=kword,
                )
            return resultado
        else:
            return self.all()[:10]

    # Consultar valores de coincidencia en un rango de fecha ingresados por parametros
    def listar_libros2(self, kword, fecha1, fecha2):
        # Con esta funcion convertimos la fecha ingresada por parametros a la fecha que utiliza nuestro modelo
        date1 = datetime.datetime.strptime(fecha1, '%Y-%m-%d').date()
        date2 = datetime.datetime.strptime(fecha1, '%Y-%m-%d').date()
        #Filtrado dentro de un rango de fecha
        resultado = self.filter(
            titulo__icontains=kword,
            fecha__range=(date1, date2),
            )
        return resultado

    # Consultar todos los valores de una determinada categoria( ForeignKey )
    def listar_libros_categoria(self, categoria):
        return self.filter(
            categoria__id = categoria
        ).order_by('titulo')

    # Insertar un valor dentro de una tabla con codigo(En este caso insertar dentro del modelo autor)
    def add_autor_libro(self, libro_id, autor):
        libro = self.get(id = libro_id)
        libro.autores.add(autor)
        return libro

    # Funcion para calcular la cantidad de veces que ha sido prestado un libro
    def libros_num_prestamos(self):
        resultado = self.aggregate(
            num_prestamos = Count('libro_prestamo')
        )

        return resultado

    # Consulta para determinar la cantidad de veces que se ha prestado un libro
    def num_libros_prestados(self):
        resultado = self.annotate(
            num_prestamos = Count('libro_prestamo')
        )

        for r in resultado:
            print('*****************')
            print(r, r.num_prestamos)
        return resultado


class CategoriaManager(models.Manager):
    """Manager para el modelo Categoria"""

    # Se define una funcion para establecer una relacion inversa entre dos tablas
    # En este caso entre Libro -> categoria cuya relacion es: Libro <- categoria
    # Consulta para saber a que categorias pertenece un escritor pasando por una tabla intermedia, en este caso Libro
    def categoria_por_autor(self, autor):
        # Se aplica el filtro para efectuar la consulta
        return self.filter(
            categoria_libro__autores__id = autor
        ).distinct() # La funcion distinct() se usa para que no se repita el mismo registro varias veces.


    # Funcion para consultar todas las categorias y la cantidad de registros que hay en cada una de ellas.
    def listar_categoria_libro(self):
        # Se usa la funcion annotate() para consultar las categorias
        resultado =  self.annotate(
            # Con esta operacion se procede a contar la cantidad de libros que pertenecen a cada categoria
            num_libros = Count('categoria_libro')
        )

        for r in resultado:
            print('************')
            print(r, r.num_libros)

        return resultado
