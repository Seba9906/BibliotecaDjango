from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
# Create your views here.

def v_prestamos(request):
    prestamos=[]
    prestamos.append(['Cien Años de Soledad','Juan Perez','28/05/1975'])
    prestamos.append(['Django dese Cero','Juan Perez','28/05/1975'])
    context = {
        'prestamos': prestamos
        

    }
    return render(request, "core/prestamos.html", context)
   