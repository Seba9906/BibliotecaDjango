from django import forms
from datetime import datetime
from django.core.exceptions import ValidationError


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
    