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
        "imagen": "\static\core\imagenes\don-quijote-de-la-mancha.webp",
        "genero": "Ficción",
    },
    2: {
        "titulo": "Libro 2",
        "autor": "Autor 2",
        "anio_publicacion": 2022,
        "imagen": "\static\core\imagenes\lotr.jpeg",
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

def v_prestamos(request):
    prestamos=[]
    prestamos.append(['Cien Años de Soledad','Juan Perez','28/05/1975'])
    prestamos.append(['Django dese Cero','Juan Perez','28/05/1975'])
    context = {
        'prestamos': prestamos
        

    }
    return render(request, "core/prestamos.html", context)
   

#VISTA DE USUARIO Y SUS LIBROS PRESTADOS

def usuario_perfil(request):
    mis_libros = [{
        'titulo': 'Cien años de soledad',
        'autor': 'Gabriel Garcia Marquez',
        'descripcion_corta': 'Historia de la familia Buendía a lo largo de 7 generaciones en el pueblo ficticio de Macondo',
        'fecha_devolucion': 'sept 30 de 2023'
    },{
        'titulo': 'Ilíada',
        'autor': 'Homero',
        'descripcion_corta': 'Relato del último año de la guerra de Troya, desde el retiro de Aquiles hasta su regreso a la batalla',
        'fecha_devolucion': 'oct 7 de 2023'
    },{
    },{
        'titulo': 'Macbeth',
        'autor': 'William Shakespeare',
        'descripcion_corta': 'Macbeth recibe la profesía de que será Rey de Escocia, por lo que decide eliminar a todos los que puedan oponerse',
        'fecha_devolucion': 'sept 23 de 2023'
    },{
        'titulo': 'Madame Bovary',
        'autor': 'Gustave Flaubert',
        'descripcion_corta': 'Emma trata de buscar el amor. Cuando al casarse descubre que no es lo que buscaba, decide tener relaciones extramaritales',
        'fecha_devolucion': 'sept 23 de 2023'
    }]

    context = {
        'nombre_usuario': 'Sam',
        'es_admin': False,
        'libros_prestados': mis_libros,
    }

    return render(request, "core/usuario_perfil.html", context)
