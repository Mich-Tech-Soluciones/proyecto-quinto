"""
Enumeraciones y opciones para el proyecto
"""

from enum import Enum


class UserRoleEnum(str, Enum):
    """Roles de usuario disponibles"""
    ADMIN = 'ADMIN'
    DESIGN = 'DESIGN'
    CUT = 'CUT'
    PRODUCTION = 'PRODUCTION'
    PACKAGING = 'PACKAGING'


class OrderStatusEnum(str, Enum):
    """Estados posibles de una orden"""
    PENDING = 'Pendiente'
    SENT = 'Enviado'
    PAID = 'Pagado'


class PaymentMethodEnum(str, Enum):
    """Métodos de pago disponibles"""
    CASH = 'Efectivo'
    CARD = 'Tarjeta'
    TRANSFER = 'Transferencia'
    CHECK = 'Cheque'


class ProductionStatusEnum(str, Enum):
    """Estados de producción"""
    PENDING = 'Pendiente'
    CUTTING = 'En Corte'
    SEWING = 'En Costura'
    QUALITY_CHECK = 'Control Calidad'
    COMPLETED = 'Completado'


class MovementTypeEnum(str, Enum):
    """Tipos de movimiento de inventario"""
    ENTRADA = 'Entrada'
    SALIDA = 'Salida'


# Diccionarios de colores para UI
STATUS_COLORS = {
    'Pendiente': '#FFC107',
    'Enviado': '#2196F3',
    'Pagado': '#4CAF50',
    'Cancelado': '#F44336',
}

PRODUCTION_STATUS_COLORS = {
    'Pendiente': '#FFC107',
    'En Corte': '#2196F3',
    'En Costura': '#9C27B0',
    'Control Calidad': '#FF9800',
    'Completado': '#4CAF50',
}
