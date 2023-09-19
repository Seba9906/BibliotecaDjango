from django.urls import path, include
from . import views
urlpatterns = [
    path("inicio/", views.index, name="index"),
    path("Modificacion/AltaLibro", views.altaLIbro, name="altaLibro"),
    path('prestamos', views.v_prestamos,name='prestamos'),
    path('usuario', views.usuario_perfil, name= 'usuario_perfil'),
    path("libro_detalle/<int:id_libro>/", views.libro_detalle, name="libro_detalle"),
]

