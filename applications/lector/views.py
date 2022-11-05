from datetime import date
from django.shortcuts import render
from django.http import HttpResponseRedirect
# Importamos las vistas a utilizar
from django.views.generic.edit import FormView
# From models
from .models import Lector, Prestamo
# From forms
from .forms import PrestamoForm, MultiplePrestamoForm


# Ejemplo de registro con un FormView
class RegistrarPrestamo(FormView):
    template_name = 'lector/add_prestamo.html'
    form_class = PrestamoForm
    success_url = '.'

    # Se utiliza la funcion form_valid para empezar a hacer procesos dentro del FormView
    # luego de haber recibido los datos desde nuestro archivo html
    def form_valid(self, form):

        # # De esta manera recogemos los datos desde el html para guardarlos
        # Prestamo.objects.create(
        #     lector = form.cleaned_data['lector'],
        #     libro  = form.cleaned_data['libro'],
        #     # Obtenemos la fecha de hoy para registrarla en nuestro modelo
        #     fecha_prestamo = date.today(),
        #     devuelto = False,
        # )

        # Esta es otra dorma de hacer lo mismo antes comentado
        prestamo = Prestamo(
            lector = form.cleaned_data['lector'],
            libro  = form.cleaned_data['libro'],
            # Obtenemos la fecha de hoy para registrarla en nuestro modelo
            fecha_prestamo = date.today(),
            devuelto = False,
        )
        prestamo.save()

        # Funcion para actualizar el numero de libros en stock
        libro  = form.cleaned_data['libro']
        libro.stock -= 1
        libro.save()

        return super(RegistrarPrestamo, self).form_valid(form)


# Ejemplo de registro con un FormView
# Dentro de esta clase se utiliza la funcion get_or_create
# La cual se utiliza para validar que una persona no pueda volver a pedir un libro sin haberlo devuelto
class AddPrestamo(FormView):
    template_name = 'lector/add_prestamo.html'
    form_class = PrestamoForm
    success_url = '.'

    # Se utiliza la funcion form_valid para empezar a hacer procesos dentro del FormView
    # luego de haber recibido los datos desde nuestro archivo html
    def form_valid(self, form):

        # Para utilizar el get_or_create primero definimos dos variables
        # obj, que va a contener el objeto en caso de que se haya creado
        # created, una variable booleana que nos va indicar si se ha creado el registro o no
        obj, created =  Prestamo.objects.get_or_create(
            # Especificamos en base a que queremos hacer el filtro
            lector = form.cleaned_data['lector'],
            libro  = form.cleaned_data['libro'],
            devuelto = False,
            defaults={
                'fecha_prestamo': date.today(),
            }
        )

        if created:
            return super(AddPrestamo, self).form_valid(form)
        else:
            return HttpResponseRedirect('/')


# Ejemplo de registro con un FormView
class AddMultiplePrestamo(FormView):
    template_name = 'lector/add_multiple_prestamo.html'
    form_class = MultiplePrestamoForm
    success_url = '.'

    # Se utiliza la funcion form_valid para empezar a hacer procesos dentro del FormView
    # luego de haber recibido los datos desde nuestro archivo html
    def form_valid(self, form):

        print(form.cleaned_data['lector'])
        print(form.cleaned_data['libros'])

        prestamos  = []

        # Recorremos el objeto libros con un for de la siguiente manera
        for l in form.cleaned_data['libros']:
            prestamo = Prestamo(
                lector = form.cleaned_data['lector'],
                libro  = l,
                # Obtenemos la fecha de hoy para registrarla en nuestro modelo
                fecha_prestamo = date.today(),
                devuelto = False,
            )
            prestamos.append(prestamo)

        # Esta funcion crea registros a partir de una lista que ya hemos creado previamente
        # En este caso va a crear registros a partir de la lista prestamos
        Prestamo.objects.bulk_create(
            prestamos
        )


        return super(AddMultiplePrestamo, self).form_valid(form)
