from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
def index(request):
    return render(request,"core/index.html")
def altaLIbro(request):
    context = {
        'fecha': datetime.now(),
    }
    return render(request,"core/altaLibro.html", context)
