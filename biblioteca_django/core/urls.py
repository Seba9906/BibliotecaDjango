from django.urls import path, include
from . import views
urlpatterns = [
    path('prestamos', views.v_prestamos,name='prestamos'),
    path('inicio/', views.index, name='index'),
    path('Modificacion/AltaLibro',views.altaLIbro,name='altaLibro'),
]
    