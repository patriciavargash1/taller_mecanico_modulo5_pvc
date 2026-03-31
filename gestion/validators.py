from django.core.exceptions import ValidationError
from django.utils import timezone
import re
from django.utils.translation import gettext_lazy as _

def validar_anio_no_futuro(value):
    anio_actual = timezone.now().year
    if value > anio_actual + 1: # Permitimos hasta el próximo año por modelos nuevos
        raise ValidationError(
            f'El año {value} no es válido. No puede ser mayor a {anio_actual + 1}.'
        )

def validar_formato_placa(valor):
    patron = r'^[A-Z]{3}\d{3}$'
    
    if not re.match(patron, valor):
        raise ValidationError(
            f'"{valor}" no es una patente válida. Debe tener 3 letras mayúsculas y 3 números (Ej: ABC123).',
            params={'valor': valor},
        )
    
def validar_costo(valor):
    if valor <= 0:  # Ejemplo: máximo 5 millones
        raise ValidationError(
            ('El costo estimado debe ser mayor a cero. Por favor, verifique el Costo estimado.'),
            code='costo_excesivo'
        )

def validar_solo_numeros(valor):
    if not valor.isdigit():
        raise ValidationError(
            _('El teléfono "%(valor)s" no es válido. No incluya espacios, guiones ni letras.'),
            params={'valor': valor},
        )
    
    # Opcional: Validar longitud mínima
    if len(valor) < 8:
        raise ValidationError(_('El número de teléfono es demasiado corto (mínimo 8 dígitos).'))   

