"""
Filtros personalizados para templates Django
"""

from django import template
from decimal import Decimal

register = template.Library()


@register.filter
def currency(value):
    """
    Formatea un valor como moneda
    """
    try:
        value = Decimal(str(value))
        return f"${value:,.2f}"
    except (ValueError, TypeError):
        return value


@register.filter
def percentage(value, decimals=2):
    """
    Formatea un valor como porcentaje
    """
    try:
        value = float(value)
        return f"{value:.{decimals}f}%"
    except (ValueError, TypeError):
        return value


@register.filter
def highlight_if(value, condition):
    """
    Resalta un valor si se cumple la condición
    """
    if condition:
        return f'<span class="highlight">{value}</span>'
    return value


@register.filter
def truncate_words(value, length=50):
    """
    Trunca un texto a una longitud específica
    """
    if len(value) > length:
        return value[:length] + "..."
    return value


@register.filter
def badge_status(value):
    """
    Retorna un badge de Bootstrap según el estado
    """
    status_badges = {
        'Completado': '<span class="badge bg-success">Completado</span>',
        'Pendiente': '<span class="badge bg-warning">Pendiente</span>',
        'Enviado': '<span class="badge bg-info">Enviado</span>',
        'Cancelado': '<span class="badge bg-danger">Cancelado</span>',
        'Pagado': '<span class="badge bg-success">Pagado</span>',
    }
    return status_badges.get(value, f'<span class="badge bg-secondary">{value}</span>')
