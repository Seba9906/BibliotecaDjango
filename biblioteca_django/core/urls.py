from django.urls import path
from . import views

urlpatterns = [
    path('',views.altaLIbro,name='altaLibro'),
]