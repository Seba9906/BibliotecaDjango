from django.urls import path, include
from . import views
urlpatterns = [
    path('prestamos', views.v_prestamos,name='prestamos')]