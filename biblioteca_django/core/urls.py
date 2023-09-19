from django.urls import path, re_path
from . import views

urlpatterns = [
    path('inicio/', views.index, name='index'),
    path('Modificacion/AltaLibro', views.altaLIbro, name='altaLibro'),
    path('usuario', views.usuario_perfil, name= 'usuario_perfil'),
]