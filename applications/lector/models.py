from django.db import models

# From db.models
from django.db.models.signals import post_delete

# From local apps.
from applications.libro.models import Libro
from applications.autor.models import Persona

# From managers
from .managers import PrestamoManager


class Lector(Persona):
    """Model definition for Lector."""

    class Meta:
        """Meta definition for Lector."""

        verbose_name = 'Lector'
        verbose_name_plural = 'Lectores'


class Prestamo(models.Model):
    lector = models.ForeignKey(
        Lector,
        on_delete=models.CASCADE
        )
    libro = models.ForeignKey(
        Libro,
        on_delete=models.CASCADE,
        # Se utiliza related_name para establecer una relacion inversa entre dos modelos
        related_name = 'libro_prestamo'
        )
    fecha_prestamo = models.DateField(
        auto_now=False,
        auto_now_add=False
        )
    fecha_devolucion = models.DateField(
        blank=True,
        null=True,
        auto_now=False,
        auto_now_add=False
        )
    devuelto = models.BooleanField()

    # Importamos el manager en nuestro modelo
    objects = PrestamoManager()

    # Redefinir la funcion save para hacer validaciones dentro de ella
    def save(self, *args, **kwargs):
        # Hacemos un procedimiento para disminuir el stock de los libros
        self.libro.stock -= 1
        self.libro.save()
        super(Prestamo, self).save(*args, **kwargs)

    def __str__(self):
        return self.libro.titulo


# Implementacion de un post_delete que nos va a aumentar el stock en un
# Al eliminar un registro de la tabla prestamo
def update_libro_stock(sender, instance, **kwargs):
    # Actualizamos el stock si se elimina un prestamo
    instance.libro.stock = instance.libro.stock + 1
    instance.libro.save()

# Llamamos a nuestro metodo post_delete
post_delete.connect(update_libro_stock, sender=Prestamo)