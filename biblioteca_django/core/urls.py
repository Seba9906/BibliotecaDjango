from django.urls import path
from . import views
<<<<<<< Updated upstream
=======
urlpatterns = [
    path("inicio/", views.index, name="index"),
    path("Modificacion/AltaLibro", views.altaLIbro, name="altaLibro"),
    path("Modificacion/modificacionLibro", views.modificacionLibro, name="modificacionLibro"),
    path('prestamos', views.v_prestamos,name='prestamos'),
    path('usuario', views.usuario_perfil, name= 'usuario_perfil'),
    path("libro_detalle/<int:id_libro>/", views.libro_detalle, name="libro_detalle"),
]
>>>>>>> Stashed changes

urlpatterns = [
    path('Modificacion/AltaLibro',views.altaLIbro,name='altaLibro'),
]