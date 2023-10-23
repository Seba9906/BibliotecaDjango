from django.urls import path, include
from . import views
from .views import RegistroUsuarioView
from .views import AutorCreateView
from .forms import *
urlpatterns = [
    path("inicio/", views.index, name="index"),
    path("Modificacion/AltaLibro", views.AltaLibro, name="altaLibro"),
    path("Modificacion/modificacionLibro", views.modificacionLibro, name="modificacionLibro"),
    path('prestamos', views.v_prestamos,name='prestamos'),
    path('usuario', views.usuario_perfil, name= 'usuario_perfil'),
    path("libro_detalle/<int:id_libro>/", views.libro_detalle, name="libro_detalle"),
    path('prestamos_form', views.prestamo_form,name='prestamos_form'),
    path('registro/', RegistroUsuarioView.as_view(), name='registro'),
    path('Modificacion/AltaAutor',AutorCreateView.as_view(),name='altaAutor')
]


