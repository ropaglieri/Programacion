from django.shortcuts import render
from .models import libro, autor, editorial, reservas, parametros_reservas
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.dispatch import Signal
from django.shortcuts import redirect

from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from django.utils import timezone

# Create your views here.
def home(request):
	return render(request, 'core/home.html')

def profile(request):
	return render(request, 'account/profile.html')

def catalogo(request):
    libros = libro.objects.all()  
    tableData = []
    for libro_obj in libros:
        data = {
            'portada': f"<img style='width: 180px;height: 180px' src='{libro_obj.portada}'>",
            'titulo': libro_obj.titulo,
            'autor': libro_obj.autor.nombre,  
            'genero': libro_obj.genero1,
            'editorial': libro_obj.editorial.nombre,  
        }
        tableData.append(data)

    return render(request, 'catalogo/catalogo.html', {'tableData': tableData})


def catalogo_elegido(request, titulo):
    libros = libro.objects.filter(titulo=titulo)
    lista_libros = {'libros': libros}

    if request.user.is_authenticated:
        usuario_logeado = True
    else:
        usuario_logeado = False

    return render(request, 'libro/libro.html', {'usuario_logeado': usuario_logeado, **lista_libros})


def reserva_libro(request, titulo):
    libros = libro.objects.filter(titulo=titulo)
    lista_libros = {'libros': libros}
    
    cantidad_disponibles = libros.first().disponibles if libros.exists() else 0

    if cantidad_disponibles <= 0:
        raise ValidationError("No hay libros disponibles para reservar.")

    return render(request, 'reserva_libro/reserva_libro.html', lista_libros)


def reserva_libro_funcionalidad(request, titulo):
    if request.method == 'POST':
        fecha_inicio_str = request.POST.get('fechaInicio')
        fecha_fin_str = request.POST.get('fechaFin')
        titulo_libro = request.POST.get('titulo')

        user = request.user
        print(user)

        try:
            libro_solicitado = libro.objects.get(titulo=titulo_libro)

            reserva_existente = reservas.objects.filter(usuario=user, titulo=libro_solicitado).exists()
            if reserva_existente:
                raise ValidationError('Ya tienes una reserva para este libro, espera a que respondan a tu solicitud.')

            fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date()
            fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d').date()

            fecha_actual = timezone.now().date()

            if fecha_inicio <= fecha_actual:
                raise ValidationError('La fecha de inicio debe ser posterior al día actual')

            if fecha_inicio >= fecha_fin:
                raise ValidationError('La fecha de fin debe ser posterior a la fecha de inicio')

            parametros_reserva = parametros_reservas.objects.first()
            tiempo_maximo_reserva = parametros_reserva.tiempo_maximo_reserva

            fecha_limite = fecha_actual + timedelta(days=tiempo_maximo_reserva)
            if fecha_fin > fecha_limite:
                raise ValidationError(f'La fecha de fin no puede ser posterior a {tiempo_maximo_reserva} días desde hoy')

            cantidad_maxima_reservada = parametros_reserva.cantidad_maxima_de_libros_reservados
            reservas_usuario = reservas.objects.filter(usuario=user).count()
            if reservas_usuario >= cantidad_maxima_reservada:
                raise ValidationError(f'Has alcanzado la cantidad máxima de libros reservados ({cantidad_maxima_reservada}).')

            reserva = reservas(usuario=user, titulo=libro_solicitado, tiempo_inicio_reserva=fecha_inicio, tiempo_fin_reserva=fecha_fin, en_espera_de_retirarse=False, ya_retirado=False, solicitud_rechazada=False)
            reserva.save()

            print('Reserva realizada con éxito')
            return redirect('catalogo')

        except libro.DoesNotExist:
            raise ValidationError('El libro no existe')

    return redirect('reserva_libro', titulo=titulo)

def perfil_usuario(request):
    usuario = request.user
    reservas_usuario = reservas.objects.filter(usuario=usuario)
    
    context = {
        'usuario': usuario,
        'reservas_usuario': reservas_usuario
    }
    
    return render(request, 'perfil_usuario/perfil_usuario.html', context)

def testeo(request):
	return render(request, 'testeo/testeo.html')
