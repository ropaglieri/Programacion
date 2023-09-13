from django.db import models
from isbn_field import ISBNField
from .choices import generos
from django.utils import timezone

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class autor(models.Model):
	nombre=models.CharField(max_length=40,verbose_name='Nombre completo')
	
	def __str__(self):
		texto="{0}"
		return texto.format(self.nombre)
	
	class Meta:
		verbose_name='Autor'
		verbose_name_plural='Autores'
		
class editorial(models.Model):
	nombre = models.CharField(max_length=30)
	pais = models.CharField(max_length=30)
	
	def __str__(self):
		texto="{0}"
		return texto.format(self.nombre)
		
	class Meta:
		verbose_name='Editorial'
		verbose_name_plural='Editoriales'


class libro(models.Model):
	titulo = models.CharField(max_length=50)
	genero1 = models.CharField(max_length=10)
	isbn = ISBNField()
	genero1 = models.CharField(max_length=20, choices=generos) 
	portada = models.CharField(max_length=70, blank=True, null=True,
			help_text="URL con imagen de la portada para visualizar.")
	autor = models.ForeignKey(autor, on_delete=models.CASCADE)
	editorial = models.ForeignKey(editorial, on_delete=models.CASCADE)
	sipnosis = models.TextField(max_length=500, blank=True, null=True)
	existencias = models.PositiveSmallIntegerField(verbose_name="Número de existencias", 
			help_text="El número de existencias totales pertenecientes a la biblioteca.")
	disponibles = models.PositiveSmallIntegerField(verbose_name="Libros disponibles al momento", 
			help_text="El número de libros que puede ser solicitado al momento.")

	def __str__(self):
		texto="{0} ({1})"
		return texto.format(self.titulo,self.isbn)
	
	def save(self, *args, **kwargs):
		if self.portada == None:
			self.portada = 'https://covers.openlibrary.org/b/isbn/'+ self.isbn + '-L.jpg'
			super(libro, self).save(*args, **kwargs)
		else:
			self.portada = 'https://covers.openlibrary.org/b/isbn/'+ self.isbn + '-L.jpg'
			super(libro, self).save(*args, **kwargs)

	class Meta:
		verbose_name='Libro'
		verbose_name_plural='Libros'


def validacion_de_inicio_reserva(value):
    hoy = timezone.now().date()
    tres_meses_despues = hoy + timezone.timedelta(days=30)
    
    if value < hoy:
        raise ValidationError("No se pueden seleccionar fechas anteriores al día de hoy.")
    
    if value > tres_meses_despues:
        raise ValidationError("No se pueden seleccionar fechas superiores a 1 mes.")

def validacion_de_fin_reserva(value):
    hoy = timezone.now().date()
    dos_meses_despues = hoy + timezone.timedelta(days=60)
    
    if value < hoy:
        raise ValidationError("No se puede seleccionar una fecha anterior al día de hoy.")
    
    if value > dos_meses_despues:
        raise ValidationError("No se puede seleccionar fechas superiores a 2 meses.")

class reservas(models.Model):
	usuario = models.ForeignKey(User, on_delete=models.CASCADE)
	titulo = models.ForeignKey(libro, on_delete=models.CASCADE)
	tiempo_inicio_reserva = models.DateField(validators=[validacion_de_inicio_reserva])
	tiempo_fin_reserva = models.DateField(validators=[validacion_de_fin_reserva])
	en_espera_de_retirarse = models.BooleanField(null=False, blank=False)
	ya_retirado = models.BooleanField(null=False, blank=False)
	solicitud_rechazada = models.BooleanField(null=False, blank=False)

	def clean(self):
		if self.tiempo_inicio_reserva and self.tiempo_fin_reserva:
			if self.tiempo_fin_reserva <= self.tiempo_inicio_reserva:
				raise ValidationError("La fecha de fin de reserva no puede ser anterior o igual a la fecha de inicio de reserva.")
				
		if self.en_espera_de_retirarse and self.ya_retirado:
			raise ValidationError("No pueden ambos estar en espera de retirarse y ya retirados al mismo tiempo.")
			
	class Meta:
		verbose_name='Reserva'
		verbose_name_plural='Reservas'
		
	def __str__(self):
		texto="{0} | {4} | {5} ({1} {2} {3})"
		return texto.format(self.titulo,self.usuario,self.en_espera_de_retirarse,self.ya_retirado,self.tiempo_inicio_reserva,self.tiempo_fin_reserva)
			
			
class parametros_reservas(models.Model):
    tiempo_maximo_reserva = models.PositiveSmallIntegerField(blank=False, null=False, verbose_name="Cantidad máximas de días de reserva", help_text="Para configurar la cantidad de días que un usuario puede llevarse un libro. NOTA: Debe colocarse un número para que se represente en días, por ejemplo 5 para 5 días.")
    cantidad_maxima_de_libros_reservados = models.PositiveSmallIntegerField(blank=False, null=False, verbose_name="Cantidad máxima de libros reservados", help_text="Para configurar el número máximo de libros que puede solicitar un usuario.")
    tiempo_espera_reserva = models.PositiveSmallIntegerField(blank=False, null=False, verbose_name="Cantidad máxima de días para buscar los libros", help_text="Para configurar el tiempo límite que tiene un usuario para presentarse en la biblioteca y preguntar por la solicitud aprobada al retirar el libro.")
    tiempo_reserva_repetida = models.PositiveSmallIntegerField(blank=False, null=False, verbose_name="Cantidad mínima de días para volver a solicitar el mismo libro", help_text="Para configurar el tiempo mínimo que un usuario debe esperar antes de solicitar el mismo libro.")
    
    class Meta:
        verbose_name='Parámetro de solicitud'
        verbose_name_plural='Parámetros de solicitudes'
    