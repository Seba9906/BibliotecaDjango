from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.urls import reverse
from datetime import datetime
from .forms import ModificacionLibroForm
from .forms import AltaLibroForm
from django.contrib import messages
from .forms import PrestamoForm  # Importa tu formulario
from .forms import RegistroUsuarioForm
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView

def prestamo_form(request):
    if request.method == 'POST':
        form = PrestamoForm(request.POST)
        if form.is_valid():
            pass
            # Procesa el formulario si es válido
            # Por ejemplo, puedes guardar los datos en la base de datos
            #titulo = form.cleaned_data['titulo']
            #autor = form.cleaned_data['autor']
            #fecha_prestamo = form.cleaned_data['fecha_prestamo']
            #nombre_usuario = form.cleaned_data['nombre_usuario']

class RegistroUsuarioView(CreateView):
    form_class = RegistroUsuarioForm
    success_url = reverse_lazy("index")  # Cambia 'inicio' por la URL de tu página de inicio.
    template_name = 'core/registro.html'

def prestamo_form(request):
    if request.method == 'POST':
        form = PrestamoForm(request.POST)
        if form.is_valid():
            # Procesa el formulario si es válido
            # Por ejemplo, puedes guardar los datos en la base de datos
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
        # Si es una solicitud GET, crea un formulario vacío
        form = PrestamoForm()
     
        return  render(request, 'core/prestamos.html')
def index(request):
    return render(request, "core/index.html")


def altaLIbro(request):
    
    if request.method == 'POST':
        #instancia con datos
        FormularioALta = AltaLibroForm(request.POST)
        #validacion
        if FormularioAlta.is_valid():
            #Mensaje de validacion

            messages.info(request,"Su operacion fue ejecutada con exito")

            return redirect(reverse("altaLibro")) 
    
    else: #GET    
        FormularioAlta = AltaLibroForm()

    context={
        "altaLibro_form" : FormularioAlta

    }
    return render(request,"core/altaLibro.html", context)


def modificacionLibro(request):

    if request.method == 'POST':
        #instancia con datos
        FormularioModificacion = ModificacionLibroForm(request.POST)
        #validacion
        if FormularioModificacion.is_valid():
            #Mensaje de validacion

            messages.info(request,"Su operacion fue ejecutada con exito")

            return redirect(reverse("modificacionLibro")) 
    
    else: #GET    
        FormularioModificacion = ModificacionLibroForm()

    context={
        "modificacionLibro_form" : FormularioModificacion

    }
    return render(request,"core/modificacionLibro.html", context)


def modificacionLibro(request):

    if request.method == 'POST':
        #instancia con datos
        FormularioModificacion = ModificacionLibroForm(request.POST)
        #validacion
        if FormularioModificacion.is_valid():
            #Mensaje de validacion

            messages.info(request,"Su operacion fue ejecutada con exito")

            return redirect(reverse("modificacionLibro")) 
    
    else: #GET    
        FormularioModificacion = ModificacionLibroForm()

    context={
        "modificacionLibro_form" : FormularioModificacion

    }
    return render(request,"core/modificacionLibro.html", context)



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
    form = PrestamoForm()
    context = {
        'prestamos': prestamos,
        'form': form,
        

    }
        # Crea una instancia del formulario
  


    # Renderiza la plantilla 'mi_template.html' con el contexto
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
