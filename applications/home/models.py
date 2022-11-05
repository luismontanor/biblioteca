import email
from pickle import TRUE
from django.db import models

class Persona(models.Model):
    """Model definition for Persona."""

    full_name = models.CharField(max_length=50)
    pais = models.CharField(max_length=50)
    pasaporte = models.CharField(max_length=50)
    edad = models.IntegerField()
    apelativo = models.CharField(max_length=10)


    class Meta:
        """Meta definition for Persona."""

        verbose_name = 'Persona'
        verbose_name_plural = 'Personas'

        # Se utiliza este atributo en el class Meta para indicarle a django que de esta manera
        # tiene que aparecer nuestro modelo en el gestor de la base de datos.
        db_table = 'persona'

        # Se usa este campo para hacer una validacion directamente en el modelo
        # Se usa unique_toguether para que no se repitan registros juntos con esas caracteristicas
        unique_together = ['pais', 'apelativo']

        # Se utiliza el atributo constraints para hacer una validacion
        # En este caso que edad sea mayor a 18
        constraints = [
            models.CheckConstraint(
                check= models.Q(edad__gte = 18),
                name='edad_mayor_18'
            )
        ]

        # Con este atributo le indicamos a django que queremos que se considere un modelo
        # pero que no se cree en nuestra base de datos ya qu lo vamos a utilizar solo para herencia
        abstract = True

    def __str__(self):
        """Unicode representation of Persona."""
        return self.full_name


# Construimos un modelo Empleado heredando los atributos del modelo Persona
class Empleados(Persona):
    empleo = models.CharField(max_length=50)


# Construimos un modelo Cliente heredando los atributos del modelo Persona
class Cliente(Persona):
    email = models.EmailField('Email', max_length=254)