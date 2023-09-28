from django import forms


class ModificacionLibroForm(forms.Form):
    titulo=forms.CharField(label="Titulo del libro", required=True)
    editorial=forms.CharField(label="Editorial", required=True)
    fechaDePublicacion=forms.DateInput()
    autor=forms.CharField(label="Autor", required=True)
    genero=forms.CharField(label="Genero literario", required=True)
    fechaDeModificacion=forms.DateTimeInput()
    caratula=forms.ImageField(label="Imagen de portada" , required=True)