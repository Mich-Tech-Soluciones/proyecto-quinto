"""
Utilidades y funciones auxiliares para el módulo de inventario
"""

from decimal import Decimal
from .models import Product, Kardex, ProductSize
from .constants import MOVEMENT_TYPE_ENTRADA, MOVEMENT_TYPE_SALIDA


def get_product_stock(product_id):
    """
    Obtiene el stock total de un producto
    
    Args:
        product_id: ID del producto
    
    Returns:
        int: Stock total del producto
    """
    try:
        product = Product.objects.get(id=product_id)
        return product.stock
    except Product.DoesNotExist:
        return 0


def get_product_profit_margin(product):
    """
    Calcula el margen de ganancia de un producto
    
    Args:
        product: Instancia del producto
    
    Returns:
        Decimal: Margen de ganancia en porcentaje
    """
    if product.cost == 0:
        return Decimal('0.00')
    
    margin = ((product.price - product.cost) / product.cost) * 100
    return Decimal(str(margin)).quantize(Decimal('0.01'))


def create_stock_movement(product, movement_type, quantity, reason, user, size=None):
    """
    Crea un movimiento en el kardex
    
    Args:
        product: Instancia del producto
        movement_type: Tipo de movimiento (Entrada/Salida)
        quantity: Cantidad del movimiento
        reason: Razón del movimiento
        user: Usuario que realiza el movimiento
        size: Talla del producto (opcional)
    
    Returns:
        Kardex: Instancia del movimiento creado
    """
    prev_stock = product.stock
    
    if movement_type == MOVEMENT_TYPE_ENTRADA:
        product.stock += quantity
    elif movement_type == MOVEMENT_TYPE_SALIDA:
        product.stock = max(0, product.stock - quantity)
    
    product.save()
    
    kardex = Kardex.objects.create(
        product=product,
        size=size,
        movement_type=movement_type,
        quantity=quantity,
        prev_stock=prev_stock,
        new_stock=product.stock,
        reason=reason,
        user=user
    )
    
    return kardex
