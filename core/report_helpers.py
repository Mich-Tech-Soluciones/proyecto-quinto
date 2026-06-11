"""
Helpers para generación de reportes
"""

from django.db.models import Sum, Count, Avg, Q
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal


def generate_sales_report(start_date=None, end_date=None):
    """
    Genera un reporte de ventas
    
    Args:
        start_date: Fecha de inicio
        end_date: Fecha de fin
    
    Returns:
        dict: Datos del reporte
    """
    from sales.models import Order
    
    if not end_date:
        end_date = timezone.now()
    
    if not start_date:
        start_date = end_date - timedelta(days=30)
    
    orders = Order.objects.filter(
        created_at__gte=start_date,
        created_at__lte=end_date
    )
    
    return {
        'total_orders': orders.count(),
        'total_sales': orders.aggregate(Sum('total'))['total__sum'] or Decimal('0.00'),
        'average_order_value': orders.aggregate(Avg('total'))['total__avg'] or Decimal('0.00'),
        'paid_orders': orders.filter(payment_status='Completado').count(),
        'pending_orders': orders.filter(payment_status__in=['Pendiente', 'Parcial']).count(),
    }


def generate_inventory_report():
    """
    Genera un reporte de inventario
    
    Returns:
        dict: Datos del reporte
    """
    from inventory.models import Product
    
    products = Product.objects.all()
    
    return {
        'total_products': products.count(),
        'total_stock_value': sum(
            p.stock * p.price for p in products
        ) or Decimal('0.00'),
        'average_stock_value': products.aggregate(Avg('price'))['price__avg'] or Decimal('0.00'),
        'low_stock_items': products.filter(stock__lte=5).count(),
        'out_of_stock_items': products.filter(stock=0).count(),
    }


def generate_production_report(start_date=None, end_date=None):
    """
    Genera un reporte de producción
    
    Args:
        start_date: Fecha de inicio
        end_date: Fecha de fin
    
    Returns:
        dict: Datos del reporte
    """
    from production.models import ProductionSheet
    
    if not end_date:
        end_date = timezone.now()
    
    if not start_date:
        start_date = end_date - timedelta(days=30)
    
    sheets = ProductionSheet.objects.filter(
        created_at__gte=start_date,
        created_at__lte=end_date
    )
    
    return {
        'total_sheets': sheets.count(),
        'completed': sheets.filter(status='Completado').count(),
        'in_progress': sheets.exclude(status='Completado').count(),
        'completion_rate': (
            (sheets.filter(status='Completado').count() / sheets.count() * 100)
            if sheets.count() > 0 else 0
        ),
    }


def generate_cost_report(start_date=None, end_date=None):
    """
    Genera un reporte de costos
    
    Args:
        start_date: Fecha de inicio
        end_date: Fecha de fin
    
    Returns:
        dict: Datos del reporte
    """
    from costs.models import Cost
    
    if not end_date:
        end_date = timezone.now()
    
    if not start_date:
        start_date = end_date - timedelta(days=30)
    
    costs = Cost.objects.filter(
        date__gte=start_date,
        date__lte=end_date
    )
    
    return {
        'total_costs': costs.aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00'),
        'number_of_costs': costs.count(),
        'average_cost': costs.aggregate(Avg('amount'))['amount__avg'] or Decimal('0.00'),
        'highest_cost': costs.aggregate(Max=Sum('amount'))['Max'] or Decimal('0.00'),
    }
