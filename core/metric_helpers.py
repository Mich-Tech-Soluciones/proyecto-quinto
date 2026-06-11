"""
Helpers para cálculo de métricas
"""

from decimal import Decimal
from django.db.models import Sum, Count, Avg, Max, Min


def calculate_profit_margin(revenue, cost):
    """
    Calcula el margen de ganancia
    
    Args:
        revenue: Ingresos
        cost: Costo
    
    Returns:
        Decimal: Margen de ganancia en porcentaje
    """
    if revenue == 0:
        return Decimal('0.00')
    
    margin = ((revenue - cost) / revenue) * 100
    return Decimal(str(margin)).quantize(Decimal('0.01'))


def calculate_roi(investment, profit):
    """
    Calcula el retorno sobre inversión
    
    Args:
        investment: Inversión inicial
        profit: Ganancia
    
    Returns:
        Decimal: ROI en porcentaje
    """
    if investment == 0:
        return Decimal('0.00')
    
    roi = (profit / investment) * 100
    return Decimal(str(roi)).quantize(Decimal('0.01'))


def calculate_growth_rate(initial_value, final_value):
    """
    Calcula la tasa de crecimiento
    
    Args:
        initial_value: Valor inicial
        final_value: Valor final
    
    Returns:
        Decimal: Tasa de crecimiento en porcentaje
    """
    if initial_value == 0:
        return Decimal('0.00')
    
    growth = ((final_value - initial_value) / initial_value) * 100
    return Decimal(str(growth)).quantize(Decimal('0.01'))


def calculate_average(queryset, field):
    """
    Calcula el promedio de un campo
    
    Args:
        queryset: QuerySet
        field: Campo a promediar
    
    Returns:
        Decimal: Promedio
    """
    result = queryset.aggregate(avg=Avg(field))
    return result['avg'] or Decimal('0.00')


def calculate_total(queryset, field):
    """
    Calcula el total de un campo
    
    Args:
        queryset: QuerySet
        field: Campo a sumar
    
    Returns:
        Decimal: Total
    """
    result = queryset.aggregate(total=Sum(field))
    return result['total'] or Decimal('0.00')


def get_statistics(queryset, field):
    """
    Obtiene estadísticas de un campo
    
    Args:
        queryset: QuerySet
        field: Campo
    
    Returns:
        dict: Estadísticas (total, promedio, máximo, mínimo, cantidad)
    """
    stats = queryset.aggregate(
        total=Sum(field),
        average=Avg(field),
        maximum=Max(field),
        minimum=Min(field),
        count=Count(field),
    )
    
    return {
        'total': stats['total'] or Decimal('0.00'),
        'average': stats['average'] or Decimal('0.00'),
        'maximum': stats['maximum'] or Decimal('0.00'),
        'minimum': stats['minimum'] or Decimal('0.00'),
        'count': stats['count'],
    }
