from django import forms
from datetime import datetime
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.contrib.auth import get_user_model
from datetime import date
from .models import *
import re
from unidecode import unidecode
from django.db.models import F
from django.utils import timezone

# ---------------------------------------------------------------------------------------------------------------------------------


class RegistroUsuarioForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Correo electronico")
    first_name = forms.CharField(required=True, label="Nombre Completo")
    last_name = forms.CharField(required=True, label="Apellido Completo")

    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "email",
            "dni",
        )

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
    cantidad = forms.IntegerField(label="Cantidad", required=True)

    class Meta:
        model = Libro
        fields = "__all__"


# ---------------------------------------------------------------------------------------------------------------------------------


class ModificacionLibroForm(forms.Form):
    titulo = forms.CharField(label="Titulo del Libro", required=True)
    editorial = forms.CharField(label="Editorial", required=True)
    Publicacion = forms.DateField(
        label="Fecha de Publicación",
        widget=forms.SelectDateWidget(years=range(1800, 2024)),
    )
    autor = forms.CharField(label="Autor", required=True)
    Stock = forms.IntegerField(label="Cantidad de Unidades")
    genero = forms.CharField(label="Genero Literario", required=True)
    Modificacion = forms.DateTimeField(
        label="Fecha y Hora Modificacion",
        widget=forms.TextInput(
            attrs={"readonly": "readonly", "class": "labelModificacion"}
        ),
        initial=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )
    caratula = forms.ImageField(label="Imagen de Portada", required=None)

    def clean_Stock(self):
        if self.cleaned_data["Stock"] > 20:
            raise ValidationError(
                "El stock maximo para cada libro es de 20 unidades por titulo"
            )

        return self.cleaned_data["Stock"]

    def clean(self):
        if self.cleaned_data["titulo"] == "Cronica de una muerte anunciada":
            raise ValidationError("El libro seleccionado ya existe")

        return self.cleaned_data


# ---------------------------------------------------------------------------------------------------------------------------------
class PrestamoForm(forms.Form):
    id_libro = forms.ModelChoiceField(
        label="Libro",
        queryset=Libro.objects.filter(
            id__in=Libro.objects.exclude(prestamo__fecha_devolucion__gt=timezone.now())
            .values("titulo")
            .annotate(first_id=F("id"))
            .order_by("titulo", "first_id")
            .distinct("titulo")
            .values("id")
        ),
        to_field_name="id",
        empty_label=None,
    )
    fecha_prestamo = forms.DateField(
        label="Fecha de Prestamo",
        initial=date.today(),
        widget=forms.widgets.DateInput(attrs={"type": "date"}),
    )
    nombre_usuario = forms.ModelChoiceField(
        label="Usuario",
        queryset=Usuario.objects.all(),
        to_field_name="username",
        empty_label=None,
    )

    def clean_fecha_prestamo(self):
        fecha_prestamo = self.cleaned_data["fecha_prestamo"]
        if fecha_prestamo > date.today():
            raise forms.ValidationError(
                "La fecha de préstamo debe ser igual o anterior a la feha actual"
            )
        return fecha_prestamo


# ---------------------------------------------------------------------------------------------------------------------------------


class altaAutor(forms.ModelForm):
    class Meta:
        model = Autor
        fields = ["nombre", "nacimiento", "pais"]

    def clean_nombre(self):
        nombre = self.cleaned_data.get("nombre")
        nombre = unidecode(nombre).lower()
        autor_existente = (
            Autor.objects.filter(nombre__iexact=nombre)
            .exclude(pk=self.instance.pk)
            .first()
        )
        if not re.match(r"^[a-zA-Z\s\-\'áéíóúÁÉÍÓÚñÑ]+$", nombre):
            raise ValidationError("Nombre inválido.")
        if autor_existente:
            raise forms.ValidationError(
                "Ya existe un autor con este nombre en la base de datos."
            )
        return nombre

    def clean_pais(self):
        pais = self.cleaned_data.get("pais")
        if not re.match(r"^[a-zA-Z\s\-\'áéíóúÁÉÍÓÚñÑ]+$", pais):
            raise ValidationError("Nombre del país inválido.")
        return pais


# ---------------------------------------------------------------------------------------------------------------------------------

Usuario = get_user_model()


class cambioContraseñaForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="Nueva contraseña", widget=forms.PasswordInput
    )
    new_password2 = forms.CharField(
        label="Confirmar nueva contraseña", widget=forms.PasswordInput
    )

    class Meta:
        model = Usuario
        fields = ("username",)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")

        # Verifica si el usuario existe
        if not Usuario.objects.filter(username=username).exists():
            raise forms.ValidationError("El usuario no existe.")

        return cleaned_data

    def save(self, commit=True):
        username = self.cleaned_data.get("username")
        user = Usuario.objects.get(username=username)
        password = self.cleaned_data.get("new_password1")
        password_confirmation = self.cleaned_data.get("new_password2")

        if password != password_confirmation:
            raise forms.ValidationError("Las contraseñas no coinciden.")

        user.set_password(password)
        if commit:
            user.save()
        return user


# ---------------------------------------------------------------------------------------------------------------------------------
class Buscador(forms.Form):
    busqueda = forms.CharField(label="Buscar")
