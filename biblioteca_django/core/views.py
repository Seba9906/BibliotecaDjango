from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse
from core.forms import *
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import Prestamo, Autor, Libro
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import logging

logging.basicConfig(level=logging.DEBUG)


# ---------------------------------------------------------------------------------------------------------------------------------
class RegistroUsuarioView(CreateView):
    form_class = RegistroUsuarioForm
    success_url = reverse_lazy("login")
    template_name = "core/registro.html"

    def form_valid(self, form):
        messages.success(self.request, "Te has registrado exitosamente!")
        return super(RegistroUsuarioView, self).form_valid(form)


# ---------------------------------------------------------------------------------------------------------------------------------


def prestamo_form(request):
    if request.method == "POST":
        form_prestamo = PrestamoForm(request.POST)

        if form_prestamo.is_valid():
            try:
                libro = form_prestamo.cleaned_data["id_libro"]
                id = request.POST.get("id_libro")
                libro = Libro.objects.get(id=id)

                usuario = form_prestamo.cleaned_data["nombre_usuario"]
                nuevo_prestamo = Prestamo(
                    libro=libro,
                    usuario=usuario,
                    fecha_prestamo=form_prestamo.cleaned_data["fecha_prestamo"],
                )
                nuevo_prestamo.save()
                messages.info(request, "El préstamo fue guardado correctamente")
                return redirect(reverse("prestamos"))

            except Libro.DoesNotExist:
                messages.error(request, "No se encontró el libro")
            except Usuario.DoesNotExist:
                messages.error(request, "No se encontró el usuario")
            except IntegrityError as e:
                messages.error(request, str(e))

            return redirect(reverse("prestamos"))
        else:
            errores = form_prestamo.errors
            return render(
                request,
                "core/prestamos.html",
                {"form": form_prestamo, "errores": errores},
            )
    else:
        form = PrestamoForm()
        return render(request, "core/prestamos.html", {"form": form})


# ---------------------------------------------------------------------------------------------------------------------------------


def index(request):
    return render(request, "core/index.html")


# ---------------------------------------------------------------------------------------------------------------------------------


def AltaLibro(request):
    if request.method == "POST":
        FormularioAlta = AltaLibroForm(request.POST, request.FILES)
        if FormularioAlta.is_valid():  # Correcto aquí
            numero = FormularioAlta.cleaned_data["cantidad"]
            for i in range(1, numero + 1):
                FormularioAlta.save()
                FormularioAlta = AltaLibroForm(request.POST, request.FILES)
            messages.info(request, "Su operacion fue ejecutada con exito")
            return redirect(reverse("altaLibro"))
    else:
        FormularioAlta = AltaLibroForm()

    context = {"altaLibro_form": FormularioAlta}

    return render(request, "core/altaLibro.html", context)


# ---------------------------------------------------------------------------------------------------------------------------------


def libro_detalle(request, id_libro):
    # Use get_object_or_404 to retrieve the Libro object or return a 404 error if not found
    libro = get_object_or_404(Libro, pk=id_libro)

    return render(request, "core/libro_detalle.html", {"libro": libro})


# ---------------------------------------------------------------------------------------------------------------------------------
def listaAutor(request):
    autores = Autor.objects.all()
    return render(request, "core/listaAutor.html", {"autores": autores})


# ---------------------------------------------------------------------------------------------------------------------------------


def listaLibro(request):
    libros = Libro.objects.all()
    return render(request, "core/listaLibro.html", {"libros": libros})


# ---------------------------------------------------------------------------------------------------------------------------------


def v_prestamos(request):
    lst_prestamos = Prestamo.objects.all()
    prestamos = []
    for p in lst_prestamos:
        prestamos.append(
            [
                p.libro.titulo,
                p.usuario.first_name + " " + p.usuario.last_name,
                p.fecha_prestamo,
            ]
        )

    form_prestamo = PrestamoForm()
    context = {
        "prestamos": prestamos,
        "form": form_prestamo,
    }

    return render(request, "core/prestamos.html", context)


# ---------------------------------------------------------------------------------------------------------------------------------


class AutorCreateView(CreateView):
    model = Autor
    form_class = altaAutor
    template_name = "core/altaAutor.html"
    success_url = reverse_lazy("altaAutor")

    def form_valid(self, form):
        messages.success(self.request, "Autor creado con éxito.")
        return super(AutorCreateView, self).form_valid(form)


# ---------------------------------------------------------------------------------------------------------------------------------


class MyLoginView(LoginView):
    template_name = "core/registration/login.html"

    def form_valid(self, form):
        messages.success(self.request, "Inicio de sesión exitoso.")
        return super().form_valid(form)


# ---------------------------------------------------------------------------------------------------------------------------------

# VISTA DE USUARIO Y SUS LIBROS PRESTADOS


@login_required
def usuario_perfil(request, user_id):
    user = get_object_or_404(Usuario, id=user_id)
    libros_prestados = request.user.prestamo_set.all()

    return render(
        request,
        "core/usuario_perfil.html",
        {"libros_prestados": libros_prestados, "user": user},
    )


# ---------------------------------------------------------------------------------------------------------------------------------


def resultados_busqueda(request):
    form = Buscador(request.GET or None)
    results = {
        "autor_results": Autor.objects.none(),
        "libro_results": Libro.objects.none(),
    }

    if request.GET and form.is_valid():
        busqueda = form.cleaned_data["busqueda"]
        logging.debug(f"Search Query: {busqueda}")

        logging.debug(f"Form Data: {form.cleaned_data}")

        autor_results = Autor.objects.filter(nombre__icontains=busqueda)
        libro_results = Libro.objects.filter(titulo__icontains=busqueda)
        results = {
            "autor_results": autor_results,
            "libro_results": libro_results,
        }

        logging.debug(f"Autores: {autor_results.count()}")
        logging.debug(f"Libros: {libro_results.count()}")

    return render(
        request, "core/resultados_busqueda.html", {"form": form, "results": results}
    )


# ---------------------------------------------------------------------------------------------------------------------------------
