"""
Utilidades y funciones auxiliares para el módulo de ventas
"""

from decimal import Decimal
from .models import Order, Payment


def calculate_order_profit(order):
    """
    Calcula la ganancia de una orden
    
    Args:
        order: Instancia de Order
    
    Returns:
        Decimal: Ganancia de la orden
    """
    total_cost = sum(detail.quantity * detail.unit_cost for detail in order.details.all())
    return order.total - total_cost


def calculate_order_margin(order):
    """
    Calcula el margen de ganancia de una orden en porcentaje
    
    Args:
        order: Instancia de Order
    
    Returns:
        Decimal: Margen de ganancia
    """
    profit = calculate_order_profit(order)
    if order.total == 0:
        return Decimal('0.00')
    
    margin = (profit / order.total) * 100
    return Decimal(str(margin)).quantize(Decimal('0.01'))


def get_payment_status_badge(payment_status):
    """
    Obtiene la clase CSS para mostrar el estado de pago como badge
    
    Args:
        payment_status: Estado del pago
    
    Returns:
        str: Clase CSS del badge
    """
    badge_classes = {
        'Pendiente': 'badge bg-warning',
        'Parcial': 'badge bg-info',
        'Completado': 'badge bg-success',
    }
    return badge_classes.get(payment_status, 'badge bg-secondary')


def get_order_status_badge(status):
    """
    Obtiene la clase CSS para mostrar el estado de orden como badge
    
    Args:
        status: Estado de la orden
    
    Returns:
        str: Clase CSS del badge
    """
    badge_classes = {
        'Pendiente': 'badge bg-secondary',
        'Enviado': 'badge bg-primary',
        'Pagado': 'badge bg-success',
    }
    return badge_classes.get(status, 'badge bg-secondary')
