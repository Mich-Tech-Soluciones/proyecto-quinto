"""
Funciones helpers globales para el proyecto
"""

from django.utils import timezone
from datetime import timedelta, datetime
from decimal import Decimal


def get_date_range(start_date=None, end_date=None, days=30):
    """
    Obtiene un rango de fechas
    
    Args:
        start_date: Fecha de inicio (opcional)
        end_date: Fecha de fin (opcional)
        days: Número de días hacia atrás (default 30)
    
    Returns:
        tuple: (start_date, end_date)
    """
    if not end_date:
        end_date = timezone.now()
    
    if not start_date:
        start_date = end_date - timedelta(days=days)
    
    return (start_date, end_date)


def format_currency(value):
    """
    Formatea un valor como moneda
    
    Args:
        value: Valor a formatear
    
    Returns:
        str: Valor formateado como moneda
    """
    try:
        value = Decimal(str(value))
        return f"${value:,.2f}"
    except (ValueError, TypeError):
        return "N/A"


def get_percentage_change(old_value, new_value):
    """
    Calcula el porcentaje de cambio
    
    Args:
        old_value: Valor anterior
        new_value: Valor nuevo
    
    Returns:
        Decimal: Porcentaje de cambio
    """
    if old_value == 0:
        return Decimal('0.00')
    
    change = ((new_value - old_value) / old_value) * 100
    return Decimal(str(change)).quantize(Decimal('0.01'))


def is_recent(date_obj, days=7):
    """
    Verifica si una fecha es reciente
    
    Args:
        date_obj: Objeto de fecha
        days: Número de días
    
    Returns:
        bool: True si es reciente
    """
    threshold = timezone.now() - timedelta(days=days)
    return date_obj >= threshold
