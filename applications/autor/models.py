from django.db import models

# From managers
from .managers import AutorManager


class Persona(models.Model):
    """Model definition for Persona."""

    nombres = models.CharField(
        max_length=50
        )
    apellidos = models.CharField(
        max_length=50
        )
    nacionalidad = models.CharField(
        max_length=20
        )
    edad = models.PositiveIntegerField()

    class Meta:
        """Meta definition for Persona."""

        abstract = True

    def __str__(self):
        """Unicode representation of Persona."""
        return str(self.id) + '-' + self.nombres + '-' + self.apellidos



class Autor(Persona):

    pseudonimo = models.CharField(
        'pseudonimo',
        max_length=50,
        blank= True
    )

    objects = AutorManager()

    class Meta:
        """Meta definition for Autor."""

        verbose_name = 'Autor'
        verbose_name_plural = 'Autores'