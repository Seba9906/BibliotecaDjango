from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime


def index(request):
    return render(request, "core/index.html")


def altaLIbro(request):
    context = {
        "fecha": datetime.now(),
    }
    return render(request, "core/altaLibro.html", context)


libros = {
    1: {
        "titulo": "Libro 1",
        "autor": "Autor 1",
        "anio_publicacion": 2021,
        "imagen": "biblioteca_django\core\static\core\imagenes\images.jpeg",
        "genero": "Ficción",
    },
    2: {
        "titulo": "Libro 2",
        "autor": "Autor 2",
        "anio_publicacion": 2022,
        "imagen": "\static\core\imagenes\images.jpeg",
        "genero": "Fantasía",
    },
}


def libro_detalle(request, id_libro):
    libro = libros.get(id_libro)

    if libro:
        libro["id"] = id_libro
        return render(request, "core/libro_detalle.html", {"libro": libro})
    else:
        return HttpResponse("Libro no encontrado")


def index(request):
    return render(request, "core/index.html")


def altaLIbro(request):
    context = {
        "fecha": datetime.now(),
    }
    return render(request, "core/altaLibro.html", context)
