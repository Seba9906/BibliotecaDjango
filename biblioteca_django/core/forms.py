from django import forms
from datetime import datetime
from django.core.exceptions import ValidationError
from datetime import date  
from .models import *
import re
from unidecode import unidecode


# ---------------------------------------------------------------------------------------------------------------------------------



class RegistroUsuarioForm(forms.ModelForm):

    contraseña = forms.CharField(widget=forms.PasswordInput)
    confirmar_contraseña = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        contraseña = cleaned_data.get("contraseña")
        confirmar_contraseña = cleaned_data.get("confirmar_contraseña")
        if contraseña and confirmar_contraseña:
            if contraseña != confirmar_contraseña:
                raise ValidationError("Las contraseñas no coinciden")
        return cleaned_data

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if not re.match(r'^[a-zA-Z\s\-\'áéíóúÁÉÍÓÚñÑ]+$', nombre):
            raise ValidationError('Nombre inválido.')
        return nombre

    def clean_apellido(self):
        apellido = self.cleaned_data.get('apellido')
        if not re.match(r'^[a-zA-Z\s\-\'áéíóúÁÉÍÓÚñÑ]+$', apellido):
            raise ValidationError('Apellido inválido.')
        return apellido

    def clean_dni(self):
        dni = self.cleaned_data.get('dni')
        if len(str(dni)) != 8:
            raise ValidationError("El DNI debe contener exactamente 8 dígitos")
        return dni
# ---------------------------------------------------------------------------------------------------------------------------------


class AltaLibroForm(forms.ModelForm):
    

    class Meta:
        model = Libro
        fields = '__all__'

    
    def clean(self):
        cleaned_data = super().clean()
        titulo = cleaned_data.get("titulo")

        titulo = unidecode(titulo).lower()

        libro_existente = Libro.objects.filter(titulo__iexact=titulo).exclude(pk=self.instance.pk).first()

        if libro_existente:
            raise forms.ValidationError("El libro con este título ya existe en la base de datos")

        return cleaned_data
# ---------------------------------------------------------------------------------------------------------------------------------


class ModificacionLibroForm(forms.Form):
    titulo=forms.CharField(label="Titulo del Libro", required=True)
    editorial=forms.CharField(label="Editorial", required=True)
    Publicacion=forms.DateField(label="Fecha de Publicación",widget=forms.SelectDateWidget(years=range(1800, 2024)))
    autor=forms.CharField(label="Autor", required=True)
    Stock=forms.IntegerField(label="Cantidad de Unidades")
    genero=forms.CharField(label="Genero Literario", required=True)
    Modificacion=forms.DateTimeField(label="Fecha y Hora Modificacion",widget=forms.TextInput(attrs={'readonly': 'readonly','class':'labelModificacion'}),initial=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    caratula=forms.ImageField(label="Imagen de Portada", required= None)

    def clean_Stock(self):
        if self.cleaned_data["Stock"] > 20:
            raise ValidationError("El stock maximo para cada libro es de 20 unidades por titulo")
        
        return self.cleaned_data["Stock"] 
    
    def clean (self):
        if self.cleaned_data["titulo"] == "Cronica de una muerte anunciada":
            raise ValidationError("El libro seleccionado ya existe")
        

        return self.cleaned_data  
# ---------------------------------------------------------------------------------------------------------------------------------
class PrestamoForm(forms.Form):
    titulo = forms.CharField(label='Título del Libro', max_length=100)
    autor = forms.CharField(label='Autor', max_length=100, required=True)
    id_libro = forms.IntegerField(label='Id Libro',required=True)
    fecha_prestamo = forms.DateField(label='Fecha de Prestamo',  
    initial=date.today(),  widget= forms.widgets.DateInput(attrs={'type':'date'}))
    nombre_usuario = forms.CharField(label='Nombre del Usuario', max_length=100)
    id_usuario = forms.IntegerField (label='Id usuario', required=True)

    def clean_fecha_prestamo(self):
        fecha_prestamo = self.cleaned_data['fecha_prestamo']
        if fecha_prestamo > date.today():
            raise forms.ValidationError("La fecha de préstamo debe ser igual o anterior a la feha actual")
        return fecha_prestamo
    
# ---------------------------------------------------------------------------------------------------------------------------------

class altaAutor(forms.ModelForm):  # He cambiado "altaAutor" a "AltaAutorForm" para seguir las convenciones de nombres en Python

    class Meta:
        model = Autor
        fields = ['nombre', 'nacimiento', 'pais']


    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        nombre = unidecode(nombre).lower()
        autor_existente = Autor.objects.filter(nombre__iexact=nombre).exclude(pk=self.instance.pk).first() 
        if not re.match(r'^[a-zA-Z\s\-\'áéíóúÁÉÍÓÚñÑ]+$', nombre):
            raise ValidationError('Nombre inválido.')
        if autor_existente:
            raise forms.ValidationError('Ya existe un autor con este nombre en la base de datos.')
        return nombre
       

    def clean_pais(self):
        pais = self.cleaned_data.get('pais')
        if not re.match(r'^[a-zA-Z\s\-\'áéíóúÁÉÍÓÚñÑ]+$', pais):
            raise ValidationError('Nombre del país inválido.')
        return pais

# ---------------------------------------------------------------------------------------------------------------------------------
