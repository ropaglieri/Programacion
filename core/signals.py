from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from .models import libro, reservas

@receiver(post_save, sender=reservas)
def actualizar_disponibilidad_libro(sender, instance, **kwargs):

    libro_relacionado = instance.titulo

  
    en_espera_anterior = instance._state.fields_cache.get("en_espera_de_retirarse", False)
    ya_retirado_anterior = instance._state.fields_cache.get("ya_retirado", False)

    if instance.en_espera_de_retirarse != en_espera_anterior:
        if instance.en_espera_de_retirarse:
            if libro_relacionado.disponibles <= 0:
                raise ValidationError("No hay libros disponibles para reservar.")
            libro_relacionado.disponibles -= 1
            print("Se restó 1 de disponibles.")
        else:
            
            libro_relacionado.disponibles += 1

  
    if instance.ya_retirado != ya_retirado_anterior:
        if instance.ya_retirado:
            
            pass
        else:
            
            libro_relacionado.disponibles += 1

   
    libro_relacionado.save()
