from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.urls import reverse
from core.forms import *
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import Prestamo, Autor, Libro
from django.db import IntegrityError


# ---------------------------------------------------------------------------------------------------------------------------------
class RegistroUsuarioView(CreateView):
    form_class = RegistroUsuarioForm
    success_url = reverse_lazy("login")  
    template_name = 'core/registro.html'
        
    def form_valid(self, form):
        
        messages.success(self.request, 'Te has registrado exitosamente!')
        return super(RegistroUsuarioView, self).form_valid(form)
    
# ---------------------------------------------------------------------------------------------------------------------------------

def prestamo_form(request):
    if request.method == 'POST':
        form_prestamo = PrestamoForm(request.POST)
        if form_prestamo.is_valid():
            try:
                libro_id = form_prestamo.cleaned_data['id_libro']
                print('ID del libro:', libro_id)  # Mantengo este print para depuración
                libro = Libro.objects.get(pk=libro_id)
                print('Libro:', libro.titulo)  # Mantengo este print para depuración

                usuario_id = form_prestamo.cleaned_data['id_usuario']
                usuario = Usuario.objects.get(id=usuario_id)

                nuevo_prestamo = Prestamo(
                    libro=libro, 
                    usuario=usuario, 
                    fecha_prestamo=form_prestamo.cleaned_data['fecha_prestamo']
                )
                nuevo_prestamo.save()
                messages.info(request, "El préstamo fue guardado correctamente")
                return redirect(reverse("prestamos"))

            except Libro.DoesNotExist:
                messages.error(request, 'No se encontró el libro')
                print('No se encontró el libro')  # Mantengo este print para depuración
            except Usuario.DoesNotExist:
                messages.error(request, 'No se encontró el usuario')
                print('No se encontró el usuario')  # Mantengo este print para depuración
            except IntegrityError as e:
                messages.error(request, str(e))
                print('Error de integridad:', e)  # Mantengo este print para depuración

            return redirect(reverse("prestamos"))
        else:
            errores = form_prestamo.errors
            print('Errores:', errores)  # Mantengo este print para depuración
            return render(request, 'core/prestamos.html', {'form': form_prestamo, 'errores': errores})
    else:
        form = PrestamoForm()
        return render(request, 'core/prestamos.html', {'form': form})

# ---------------------------------------------------------------------------------------------------------------------------------

def index(request):
    return render(request, "core/index.html")
# ---------------------------------------------------------------------------------------------------------------------------------


def AltaLibro(request):
    
    if request.method == 'POST':

        FormularioAlta = AltaLibroForm(request.POST, request.FILES) 
        if FormularioAlta.is_valid():  # Correcto aquí
            numero = FormularioAlta.cleaned_data['cantidad']
            print(numero)
            for i in range(1,numero+1):
                FormularioAlta.save()
                FormularioAlta = AltaLibroForm(request.POST, request.FILES) 
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
def listaAutor(request):
    autores = Autor.objects.all()
    return render(request, "core/listaAutor.html", {'autores': autores})

# ---------------------------------------------------------------------------------------------------------------------------------

def listaLibro(request):
    libros = Libro.objects.all()
    return render(request, "core/listaLibro.html", {'libros': libros})

# ---------------------------------------------------------------------------------------------------------------------------------

def v_prestamos(request):
    lst_prestamos=Prestamo.objects.all()
    prestamos=[]
    for p in lst_prestamos:
        prestamos.append([p.libro.titulo,p.usuario.first_name+ ' '+p.usuario.last_name,p.fecha_prestamo])
       
    form_prestamo = PrestamoForm()
    context = {
        'prestamos': prestamos,
        'form': form_prestamo,
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

class MyLoginView(LoginView):
    template_name = 'core/registration/login.html'
    

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
