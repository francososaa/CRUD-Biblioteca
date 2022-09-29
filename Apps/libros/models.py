# DJANGO
import uuid
from django.db import models

class Autor(models.Model):

    id = models.AutoField('ID', primary_key=True)
    nombre = models.CharField('Nombre', max_length=100, null=False, blank=False)
    apellido = models.CharField('Apellido', max_length=100, null=False, blank=False)
    nacionalidad = models.CharField('Nacionalidad', max_length=100, null=False, blank=False)
    fecha_creacion = models.DateField('Fecha de creacion', auto_now=False, auto_now_add=True)
    estado = models.BooleanField('Estado', default=True)

    class Meta:
        verbose_name = 'autor'
        verbose_name_plural = 'autores'
        ordering = ['id']

    def __str__(self):
        return '{} {}'.format(self.apellido, self.nombre)

class Libro(models.Model):

    tipo_libro = [
        ('Seleccionar', 'Seleccionar'),
        ('Ficcion', 'Ficcion'),
        ('Suspenso', 'Suspenso'),
        ('Ciencia Ficcion', 'Ciencia Ficcion'),
        ('Terror', 'Terror'),
        ('Policial', 'Policial'),
    ]

    id = models.AutoField(primary_key=True)
    isbn = models.UUIDField('ISBN', default=uuid.uuid4, editable=False)
    titulo = models.CharField('Titulo', max_length=100, null=False, blank=False, unique=True)
    editorial = models.CharField('Editorial', max_length=100, null=False, blank=False)
    paginas = models.IntegerField('Numero de Paginas', null=False, blank=False)
    publicacion = models.CharField('Publicacion', max_length=100)
    clasificacion = models.CharField('Clasificacion', max_length=15, choices=tipo_libro, default='Seleccionar')
    sinopsis = models.TextField('Sinopsis', max_length=3000, null=False, blank=False)
    estado = models.BooleanField('Estado', default=True)
    autor = models.ManyToManyField(Autor, related_name='autor')

    class Meta:
        verbose_name = 'libro'
        verbose_name_plural = 'libros'
        ordering = ['id']
    
    def __str__(self):
        return self.titulo