from django import forms
from datetime import datetime
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from datetime import date  
from .models import *
import re


# ---------------------------------------------------------------------------------------------------------------------------------



class RegistroUsuarioForm(UserCreationForm):
    email = forms.EmailField(required=True,label='Correo electronico')
    first_name = forms.CharField(required=True,label='Nombre Completo')
    last_name = forms.CharField(required=True,label='Apellido Completo')

    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email', 'dni',)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user
# ---------------------------------------------------------------------------------------------------------------------------------


class AltaLibroForm(forms.ModelForm):
    
    cantidad = forms.IntegerField(label='Cantidad de ejemplares')
    class Meta:
        model = Libro
        fields = '__all__'
    def clean_numero(self):
        if self.cleaned_data["Stock"] >0:
            raise ValidationError("La cantidad debe ser mayor a 1")
        return self.cleaned_data["numero"] 
    def clean_Stock(self):
        if self.cleaned_data["Stock"] > 20:
            raise ValidationError("El stock maximo para cada libro es de 20 unidades por titulo")
        
        return self.cleaned_data["Stock"] 
    
    def clean (self):
        if self.cleaned_data["titulo"] == "Cronica de una muerte anunciada":
            raise ValidationError("El libro seleccionado ya existe")
        

        return self.cleaned_data  

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
        if not re.match(r'^[a-zA-Z\s\-\'áéíóúÁÉÍÓÚñÑ]+$', nombre):
            raise ValidationError('Nombre inválido.')
        return nombre
    def clean_pais(self):
        pais = self.cleaned_data.get('pais')
        if not re.match(r'^[a-zA-Z\s\-\'áéíóúÁÉÍÓÚñÑ]+$', pais):
            raise ValidationError('Nombre del país inválido.')
        return pais

# ---------------------------------------------------------------------------------------------------------------------------------
