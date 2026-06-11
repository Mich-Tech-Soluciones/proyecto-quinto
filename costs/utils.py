"""
Utilidades y funciones auxiliares para el módulo de costos
"""

from decimal import Decimal
from django.db.models import Sum
from .models import Cost


def get_total_costs_by_order(order):
    """
    Obtiene el total de costos para una orden
    
    Args:
        order: Instancia de Order
    
    Returns:
        Decimal: Total de costos
    """
    total = Cost.objects.filter(order=order).aggregate(total=Sum('amount'))
    return total['total'] or Decimal('0.00')


def get_costs_summary(order):
    """
    Obtiene un resumen de costos para una orden
    
    Args:
        order: Instancia de Order
    
    Returns:
        dict: Resumen con total, promedio, máximo y mínimo
    """
    costs = Cost.objects.filter(order=order)
    total_costs = sum(cost.amount for cost in costs) if costs else Decimal('0.00')
    
    if not costs:
        return {
            'total': Decimal('0.00'),
            'count': 0,
            'average': Decimal('0.00'),
        }
    
    return {
        'total': total_costs,
        'count': costs.count(),
        'average': total_costs / costs.count() if costs.count() > 0 else Decimal('0.00'),
    }


def get_production_cost_percentage(order):
    """
    Calcula el porcentaje de costo de producción respecto al total del pedido
    
    Args:
        order: Instancia de Order
    
    Returns:
        Decimal: Porcentaje del costo
    """
    if order.total == 0:
        return Decimal('0.00')
    
    total_costs = get_total_costs_by_order(order)
    percentage = (total_costs / order.total) * 100
    return Decimal(str(percentage)).quantize(Decimal('0.01'))
