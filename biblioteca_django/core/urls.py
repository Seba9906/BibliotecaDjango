from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from .views import RegistroUsuarioView, AutorCreateView, MyLoginView
from .forms import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView 

urlpatterns = [
    path("inicio/", views.index, name="index"),
    path("Modificacion/AltaLibro", views.AltaLibro, name="altaLibro"),
    path("Modificacion/modificacionLibro",views.modificacionLibro,name="modificacionLibro",),
    path("listaAutor/", views.listaAutor, name="listaAutor"),
    path("listaLibro/", views.listaLibro, name="listaLibro"),
    path("prestamos", views.v_prestamos, name="prestamos"),
    path("usuario/<int:user_id>/", views.usuario_perfil, name="usuario_perfil"),
    path("libro_detalle/<int:id_libro>/",views.libro_detalle, name="libro_detalle"),
    path("prestamos_form", views.prestamo_form, name="prestamos_form"),
    path("registro/", RegistroUsuarioView.as_view(), name="registro"),
    path("Modificacion/AltaAutor", AutorCreateView.as_view(), name="altaAutor"),
    path("resultados_busqueda/", views.resultados_busqueda,name="resultados_busqueda"),
    path("accounts/login/", MyLoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name='logout'),
    path("accounts/password_change/",auth_views.PasswordChangeView.as_view(template_name="core/registration/password_change_form.html"),name="password_change",),
    path("accounts/password_change/done/",auth_views.PasswordChangeDoneView.as_view(template_name="core/registration/password_change_done.html"),name="password_change_done",),
    path("accounts/password_reset/",auth_views.PasswordResetView.as_view(template_name="core/registration/password_reset_form.html"),name="password_reset",),
    path("accounts/password_reset/done/",auth_views.PasswordResetDoneView.as_view(template_name="core/registration/password_reset_done.html"),name="password_reset_done",),
    path("accounts/reset/<uidb64>/<token>/",auth_views.PasswordResetConfirmView.as_view(template_name="core/registration/password_reset_confirm.html"),name="password_reset_confirm",),
    path("accounts/reset/done/",auth_views.PasswordResetCompleteView.as_view(template_name="core/registration/password_reset_complete.html"),name="password_reset_complete",),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
