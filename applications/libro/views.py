from django.shortcuts import render

from django.views.generic import (
    ListView,
    DetailView,
)
from .models import Libro


class ListLibros(ListView):
    #model = Autor
    context_object_name= 'lista_libro'
    template_name = "libro/lista_libros.html"

    def get_queryset(self):
        palabra_clave = self.request.GET.get("kword", '')

        # Fecha 1
        f1 = self.request.GET.get("fecha1", '')
        # Fecha 2
        f2 = self.request.GET.get("fecha2", '')

        if(f1 and f2):
            return Libro.objects.listar_libros2(palabra_clave, f1, f2)
        else:
            return Libro.objects.listar_libros(palabra_clave)


class ListLibrosTrg(ListView):
    #model = Autor
    context_object_name= 'lista_libro'
    template_name = "libro/lista_libros.html"

    def get_queryset(self):
        palabra_clave = self.request.GET.get("kword", '')

        return Libro.objects.listar_libros_trg(palabra_clave)


class ListLibros2(ListView):
    #model = Autor
    context_object_name= 'lista_libro'
    template_name = "libro/lista_libros2.html"

    def get_queryset(self):

        parametro='5'
        return Libro.objects.listar_libros_categoria(parametro)


class LibroDetailView(DetailView):
    model = Libro
    template_name = "libro/detalle.html"
