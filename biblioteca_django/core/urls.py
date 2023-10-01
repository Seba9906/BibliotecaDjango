from django.urls import path, include
from . import views
urlpatterns = [
    path("inicio/", views.index, name="index"),
    path("Modificacion/AltaLibro", views.altaLIbro, name="altaLibro"),
    path("Modificacion/modificacionLibro", views.modificacionLibro, name="modificacionLibro"),
]
