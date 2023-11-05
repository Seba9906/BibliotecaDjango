from typing import Any
from django.contrib import admin
from django.db.models.fields.related import ManyToManyField
from django.forms.models import ModelMultipleChoiceField
from django.http.request import HttpRequest
from core.models import Usuario,Autor,Libro,Prestamo

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('dni' , 'apellido','nombre', 'email', 'contraseña')
    list_editable = ('apellido', 'nombre', 'email', 'contraseña')
    list_display_links=['dni']
    search_fields = ['apellido']

class AutorAdmin(admin.ModelAdmin):
    list_display = ('nombre','nacimiento', 'pais')
    list_editable = ('nacimiento', 'pais')
    list_display_links=['nombre']
    search_fields = ['nombre']

class LibroAdmin(admin.ModelAdmin):
    list_display=('titulo', 'editorial','publicacion','genero') 
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'autores':
            kwargs['queryset'] = Autor.objects.filter(nacimiento__startswith='1').orderby('nombre')
        return super().formfield_for_manytomany(db_field, request, **kwargs)       

admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Autor, AutorAdmin)
admin.site.register(Libro)
admin.site.register(Prestamo)

# Register your models here.
