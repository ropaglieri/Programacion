from .views import home, profile, catalogo, testeo, catalogo_elegido, reserva_libro, perfil_usuario, reserva_libro_funcionalidad
from django.urls import path, include


urlpatterns = [
    path('', home, name='home'),
    path('accounts/profile/', profile, name='profile'),
    path('catalogo/', catalogo, name='catalogo'),
    path('catalogo/<str:titulo>', catalogo_elegido, name='catalogo_elegido'),
    path('catalogo/<str:titulo>/reserva_libro/', reserva_libro, name='reserva_libro'),
    path('testeo/', testeo, name='testeo'),
    path('perfil_usuario/', perfil_usuario, name='perfil_usuario'),
    path('catalogo/<str:titulo>/reserva_libro/reserva_libro_funcionalidad/', reserva_libro_funcionalidad, name='reserva_libro_funcionalidad'),
    ]
