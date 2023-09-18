from django.urls import path
from . import views

urlpatterns = [
    path('Modificacion/AltaLibro',views.altaLIbro,name='altaLibro'),
]