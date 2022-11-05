from importlib.metadata import requires
from urllib import request
from django import forms

# From libro.models
from applications.libro.models import Libro

# From models
from .models import Prestamo


class PrestamoForm(forms.ModelForm):
    """Form definition for Prestamo."""

    class Meta:
        """Meta definition for Prestamoform."""

        model = Prestamo
        fields = (
            'lector',
            'libro',
        )


class MultiplePrestamoForm(forms.ModelForm):
    """Form definition for Prestamo."""

    # Con este procedimiento construimos una lista con los libros que puedan ser seleccionados
    # De esta manera relacionamos la lista directamente con un modelo
    libros = forms.ModelMultipleChoiceField(
        # Indicamos el origen del cual queremos obtener los datos
        queryset=None,
        required=True,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        """Meta definition for MultiplePrestamoForm."""

        model = Prestamo
        fields = (
            'lector',
        )

    def __init__(self, *args, **kwargs):
        super(MultiplePrestamoForm, self).__init__(*args, **kwargs)
        # Con esta linea de codigo obtenemos todos los libros y los agregamos en una lista
        self.fields['libros'].queryset = Libro.objects.all()