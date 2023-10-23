from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.urls import reverse
from datetime import datetime
from core.forms import *
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView


# ---------------------------------------------------------------------------------------------------------------------------------


class RegistroUsuarioView(CreateView):
    form_class = RegistroUsuarioForm
    success_url = reverse_lazy("index")  
    template_name = 'core/registro.html'
# ---------------------------------------------------------------------------------------------------------------------------------

def prestamo_form(request):
    if request.method == 'POST':
        form = PrestamoForm(request.POST)
        if form.is_valid():
          
            #titulo = form.cleaned_data['titulo']
            #autor = form.cleaned_data['autor']
            #fecha_prestamo = form.cleaned_data['fecha_prestamo']
            #nombre_usuario = form.cleaned_data['nombre_usuario']

            messages.info(request,"El prestamo fue guardado correctamente")

            return redirect(reverse("prestamos")) 

        else:
            errores = form.errors
            print(errores)
            return  render(request, 'core/prestamos.html', {'form': form, 'errores': errores})

    else:
      
        form = PrestamoForm()
     
        return  render(request, 'core/prestamos.html')
# ---------------------------------------------------------------------------------------------------------------------------------

def index(request):
    return render(request, "core/index.html")
# ---------------------------------------------------------------------------------------------------------------------------------


def AltaLibro(request):
    
    if request.method == 'POST':

        FormularioAlta = AltaLibroForm(request.POST, request.FILES) #necesito el request files para cargar la caratula del altalibro

        if FormularioAlta.is_valid():  # Correcto aquí
            FormularioAlta.save()
            messages.info(request, "Su operacion fue ejecutada con exito")
            return redirect(reverse("altaLibro")) 
    else:    
        FormularioAlta = AltaLibroForm()

    context = {
        "altaLibro_form" : FormularioAlta
    }

    return render(request, "core/altaLibro.html", context)

# ---------------------------------------------------------------------------------------------------------------------------------

def modificacionLibro(request):

    if request.method == 'POST':

        FormularioModificacion = ModificacionLibroForm(request.POST)

        if FormularioModificacion.is_valid():


            messages.info(request,"Su operacion fue ejecutada con exito")

            return redirect(reverse("modificacionLibro")) 
    
    else:   
        FormularioModificacion = ModificacionLibroForm()

    context={
        "modificacionLibro_form" : FormularioModificacion

    }
    return render(request,"core/modificacionLibro.html", context)

# ---------------------------------------------------------------------------------------------------------------------------------


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

# ---------------------------------------------------------------------------------------------------------------------------------

def libro_detalle(request, id_libro):
    libro = libros.get(id_libro)

    if libro:
        libro["id"] = id_libro
        return render(request, "core/libro_detalle.html", {"libro": libro})
    else:
        return HttpResponse("Libro no encontrado")
# ---------------------------------------------------------------------------------------------------------------------------------

def v_prestamos(request):
    prestamos=[]
    prestamos.append(['Cien Años de Soledad','Juan Perez','28/05/1975'])
    prestamos.append(['Django dese Cero','Juan Perez','28/05/1975'])
    form = PrestamoForm()
    context = {
        'prestamos': prestamos,
        'form': form,
    }
    return render(request, "core/prestamos.html", context)
   
# ---------------------------------------------------------------------------------------------------------------------------------
   
class AutorCreateView(CreateView):
    model = Autor
    form_class = altaAutor
    template_name = 'core/altaAutor.html'
    success_url = reverse_lazy('altaAutor')  
    
    def form_valid(self, form):
        messages.success(self.request, 'Autor creado con éxito.')
        return super(AutorCreateView, self).form_valid(form)

    
# ---------------------------------------------------------------------------------------------------------------------------------

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
# ---------------------------------------------------------------------------------------------------------------------------------
