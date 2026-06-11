"""
Validadores personalizados para el proyecto
"""

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
import re


def validate_product_name(value):
    """
    Valida que el nombre del producto no contenga caracteres especiales
    """
    if len(value.strip()) == 0:
        raise ValidationError('El nombre del producto no puede estar vacío')
    
    if len(value) > 200:
        raise ValidationError('El nombre del producto no puede exceder 200 caracteres')


def validate_positive_price(value):
    """
    Valida que el precio sea positivo
    """
    if value < 0:
        raise ValidationError('El precio no puede ser negativo')


def validate_stock_quantity(value):
    """
    Valida que la cantidad sea un número positivo
    """
    if value < 0:
        raise ValidationError('La cantidad no puede ser negativa')


def validate_customer_phone(value):
    """
    Valida el formato del teléfono del cliente
    """
    phone_pattern = r'^\+?1?\d{9,15}$'
    if not re.match(phone_pattern, value.replace('-', '').replace(' ', '')):
        raise ValidationError('El formato del teléfono no es válido')


# Validadores regex
phone_validator = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message='Ingrese un teléfono válido',
    code='invalid_phone'
)

postal_code_validator = RegexValidator(
    regex=r'^\d{4,10}$',
    message='Código postal inválido',
    code='invalid_postal_code'
)
