from django.contrib import admin
from .models import libro
from .models import autor
from .models import editorial
from .models import reservas
from .models import parametros_reservas

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

class UsuarioInline(admin.StackedInline):
    model = reservas
    can_delete = False
    verbose_name_plural = "usuarios"


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = [UsuarioInline]


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(libro)
class GestionLibro(admin.ModelAdmin):
	list_display=('id','titulo', 'autor', 'genero1', 'isbn', 'existencias', 'disponibles')
	ordering = ('id',)
	search_fields=('titulo', 'autor__nombre', 'isbn', 'existencias', 'disponibles')
	list_per_page= 10
	autocomplete_fields=('autor','editorial')

	fieldsets=(
		(None,{
			'fields':('titulo', 'autor', 'isbn', 'editorial', 'genero1', 'sipnosis', 'existencias', 'disponibles')
			}),
		('Opciones avanzadas',{
			'classes':('collapse','wide','extrapretty'),
			'fields':('portada',)
			})
	)

@admin.register(autor)
class GestionAutor(admin.ModelAdmin):
	list_display=('id','nombre')
	ordering = ('nombre',)
	search_fields=('nombre',)
	list_per_page= 10

@admin.register(editorial)
class GestionEditorial(admin.ModelAdmin):
	list_display=('id','nombre', 'pais')
	ordering = ('id',)
	search_fields=('nombre','pais')
	list_per_page= 10


@admin.register(reservas)
class GestionReserva(admin.ModelAdmin):
	readonly_fields=('id',)
	list_display=('id','usuario','titulo','tiempo_inicio_reserva','tiempo_fin_reserva','en_espera_de_retirarse','ya_retirado')
	ordering = ('id',)
	search_fields=('id','usuario','titulo','tiempo_inicio_reserva','tiempo_fin_reserva','en_espera_de_retirarse','ya_retirado')
	autocomplete_fields = ('titulo','usuario')
	list_per_page= 10
	
	
@admin.register(parametros_reservas)
class GestionParametrosReservas(admin.ModelAdmin):
    list_display=('tiempo_maximo_reserva', 'cantidad_maxima_de_libros_reservados', 'tiempo_espera_reserva', 'tiempo_reserva_repetida')
    
    def no_permitir_mas_de_uno(self, request): # Here
        return not parametros_reservas.objects.exists()

    
    
    
    