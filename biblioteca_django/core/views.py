from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.urls import reverse
from datetime import datetime
<<<<<<< Updated upstream
# Create your views here.
=======
from .forms import ModificacionLibroForm
from django.contrib import messages


def index(request):
    return render(request, "core/index.html")

>>>>>>> Stashed changes

def altaLIbro(request):
    context = {
        'fecha': datetime.now(),

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



    }


    return render(request,"core/altaLibro.html", context)
