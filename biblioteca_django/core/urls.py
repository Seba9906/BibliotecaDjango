from django.urls import path, re_path
from . import views

urlpatterns = [
    path("inicio/", views.index, name="index"),
    path("Modificacion/AltaLibro", views.altaLIbro, name="altaLibro"),
    path("libro_detalle/<int:id_libro>/", views.libro_detalle, name="libro_detalle"),
]
