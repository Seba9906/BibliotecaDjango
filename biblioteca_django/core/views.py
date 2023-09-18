from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
# Create your views here.

def altaLIbro(request):
    context = {
        'fecha': datetime.now(),


    }


    return render(request,"core/altaLibro.html", context)
