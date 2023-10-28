from django.db import models
from django.core.exceptions import ValidationError
from datetime import timedelta
import re

GENRE_CHOICES = (
    ('FIC', 'Ficción'),
    ('NFIC', 'No Ficción'),
    ('SF', 'Ciencia Ficción'),
    ('MYST', 'Misterio'),
    ('ROM', 'Romance'),
    ('DRAMA', 'Drama'),
    ('FANT', 'Fantasía'),
    ('BIO', 'Biografía'),
    ('ACAD', 'Artículos Académicos'),
)

class Usuario(models.Model):
      
      nombre = models.CharField(max_length=30,verbose_name="nombre")
      apellido = models.CharField(max_length=30,verbose_name="apellido")
      dni = models.IntegerField(verbose_name="Dni", unique=True)
      email = models.EmailField(max_length=150, verbose_name="Email")
      contraseña = models.CharField(max_length=50,verbose_name="contraseña",default="")
      def __str__(self):
        return self.nombre
         
class Autor(models.Model):
      nombre = models.CharField(max_length=100, verbose_name="Nombre y Apellido del Autor/a")
      pais = models.CharField(max_length=100,verbose_name="Nacionalidad del Autor/a")
      nacimiento = models.IntegerField(verbose_name="Año de nacimiento del Autor/a")

      def __str__(self):
        return self.nombre
    
class Libro(models.Model):
    titulo = models.CharField(max_length=255, verbose_name="Título del Libro")
    autores = models.ManyToManyField(Autor, verbose_name="Autor/a o Autor@s del Libro")
    editorial = models.CharField(max_length=255,verbose_name="Editorial")
    publicacion = models.IntegerField(verbose_name="Año de publicación")
    genero = models.CharField(max_length=100, choices=GENRE_CHOICES)

    def __str__(self):
        return self.titulo
  
class Prestamo(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name="Usuario")
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE, verbose_name="Libro Prestado")
    fecha_prestamo = models.DateField(verbose_name="Fecha de Préstamo")
    fecha_devolucion = models.DateField(verbose_name="Fecha de Devolución")

    def save(self, *args, **kwargs):
        if not self.fecha_devolucion:
            self.fecha_devolucion = self.fecha_prestamo + timedelta(days=14)
        super(Prestamo, self).save(*args, **kwargs)

    def __str__(self):
        return f"Prestamo de {self.libro} a {self.usuario} retirado {self.fecha_prestamo} devolucion {self.fecha_devolucion}"

       