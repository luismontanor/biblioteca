from pickletools import optimize
from tabnanny import verbose
from django.db import models

# From db.models
from django.db.models.signals import post_save

# Apps de terceros
from PIL import Image

# From local apps.
from applications.autor.models import Autor

# Import managers
from .managers import LibroManager, CategoriaManager


class Categoria(models.Model):
    nombre = models.CharField(max_length=50)

    objects = CategoriaManager()

    def __str__(self):
        return str(self.id) + '-' + self.nombre


class Libro(models.Model):
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        # Se define este campo para establecer una relacion inversa entre dos tablas habiendo una tabla intermedia
        # En este caso entre Libro -> categoria cuya relacion es: Libro <- categoria, la tabla intermedia es Libro
        related_name='categoria_libro'
        )
    autores = models.ManyToManyField(Autor)
    titulo = models.CharField(max_length=50)
    fecha = models.DateField(
        'Fehca de lanzamiento',
        auto_now=False,
        auto_now_add=False
        )
    portada = models.ImageField(
        upload_to='portada',
        height_field=None,
        width_field=None,
        max_length=None
        )
    visitas = models.PositiveIntegerField()
    stock = models.PositiveIntegerField(default=0)

    # Importamos el manager en nnuestro modelo
    objects = LibroManager()

    class Meta:
        verbose_name = 'Libro'
        verbose_name_plural = 'Libros'
        ordering = ['titulo', 'fecha']

    def __str__(self):
        return str(self.id) + '-' + self.titulo


# Funcion para optimizar una imagen despues de cargarla a nuestra base de datos
def optimize_image(sender, instance, **kwargs):
    print('********************')
    if instance.portada:
        portada = Image.open(instance.portada.path)
        portada.save(instance.portada.path, quality=20, optimize=True)

# El post_save se encarga de ejecutar las operaciones definidas anteriormente
# Y luego guardar en los archivos en nuestra base de datos
post_save.connect(optimize_image, sender=Libro)