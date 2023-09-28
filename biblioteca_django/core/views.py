from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
<<<<<<< Updated upstream
# Create your views here.
=======
from .forms import ModificacionLibroForm


def index(request):
    return render(request, "core/index.html")

>>>>>>> Stashed changes

def altaLIbro(request):
    context = {
        'fecha': datetime.now(),

def modificacionLibro(request):

    FormularioModificacion = ModificacionLibroForm()

    context={
        "modificacionLibro_form" : FormularioModificacion

    }
    return render(request,"core/modificacionLibro.html", context)



    }


    return render(request,"core/altaLibro.html", context)
