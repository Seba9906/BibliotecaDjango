from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from datetime import timedelta
import re

GENRE_CHOICES = (
    ("FIC", "Ficción"),
    ("NFIC", "No Ficción"),
    ("SF", "Ciencia Ficción"),
    ("MYST", "Misterio"),
    ("ROM", "Romance"),
    ("DRAMA", "Drama"),
    ("FANT", "Fantasía"),
    ("BIO", "Biografía"),
    ("ACAD", "Artículos Académicos"),
)


class Usuario(AbstractUser):
    dni = models.IntegerField("DNI", unique=True, null=True, blank=True)

    def _str_(self):
        return f"{self.first_name} {self.last_name}"


class Autor(models.Model):
    nombre = models.CharField(
        max_length=100, verbose_name="Nombre y Apellido del Autor/a"
    )
    pais = models.CharField(max_length=100, verbose_name="Nacionalidad del Autor/a")
    nacimiento = models.IntegerField(verbose_name="Año de nacimiento del Autor/a")

    def __str__(self):
        return self.nombre


class Libro(models.Model):
    autores = models.ManyToManyField(Autor, verbose_name="Autor/a o Autor@s del Libro")
    titulo = models.CharField(max_length=255, verbose_name="Título del Libro")
    editorial = models.CharField(max_length=255, verbose_name="Editorial")
    publicacion = models.IntegerField(verbose_name="Año de publicación")
    genero = models.CharField(max_length=100, choices=GENRE_CHOICES)
    imagen = models.ImageField(upload_to="media/", default="default_book_cover.png")

    def __str__(self):
        return self.titulo


class Prestamo(models.Model):
    usuario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, verbose_name="Usuario"
    )
    libro = models.ForeignKey(
        Libro, on_delete=models.CASCADE, verbose_name="Libro Prestado"
    )
    fecha_prestamo = models.DateField(verbose_name="Fecha de Préstamo")
    fecha_devolucion = models.DateField(verbose_name="Fecha de Devolución")

    def save(self, *args, **kwargs):
        if not self.fecha_devolucion:
            self.fecha_devolucion = self.fecha_prestamo + timedelta(days=14)
        super(Prestamo, self).save(*args, **kwargs)

    def __str__(self):
        return f"Prestamo de {self.libro} a {self.usuario} retirado {self.fecha_prestamo} devolucion {self.fecha_devolucion}"
