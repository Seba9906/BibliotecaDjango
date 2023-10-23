from django.db import models
from django.core.exceptions import ValidationError
from datetime import timedelta
import re
class Usuario(models.Model):
      
      nombre = models.CharField(max_length=30,verbose_name="nombre")
      apellido = models.CharField(max_length=30,verbose_name="apellido")
      dni = models.IntegerField(verbose_name="Dni", unique=True)
      email = models.EmailField(max_length=150, verbose_name="Email")
      
      def clean_nombre(self):
            nombre = self.nombre
            if not re.match(r'^[a-zA-Z\s\-\'áéíóúÁÉÍÓÚñÑ]+$', nombre):
                  raise ValidationError('Nombre Invalido.')
            return self.cleaned_data['nombre']

      def clean_apellido(self):
            apellido = self.apellido
            if not re.match(r'^[a-zA-Z\s\-\'áéíóúÁÉÍÓÚñÑ]+$', apellido):
                  raise ValidationError('Apellido Invalido.')
            return self.cleaned_data['apellido']

      def clean_dni(self):
            if len(str(self.dni)) != 8:
                  raise ValidationError("El Dni contener exactamente 8 digitos")
            return self.cleaned_data['dni']
      
class Autor(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class Libro(models.Model):
    titulo = models.CharField(max_length=255, verbose_name="Título del Libro")
    editorial = models.CharField(max_length=255,verbose_name="Editorial")
    publicacion = models.IntegerField(verbose_name="fecha de publicación")
    autores = models.ManyToManyField(Autor, verbose_name="Autor/a o Autor@s del Libro")
    stock = models.IntegerField(default=1)
    genero = models.CharField(max_length=255,verbose_name="Genero")
    modificacion = models.DateTimeField(auto_now=True)
    caratula = models.ImageField(upload_to='core/static/core/imagenes',default=None)

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