"""
Constantes para la aplicación de ventas
"""

# Estados de orden
ORDER_STATUS_PENDING = 'Pendiente'
ORDER_STATUS_CONFIRMED = 'Confirmada'
ORDER_STATUS_SHIPPED = 'Enviada'
ORDER_STATUS_DELIVERED = 'Entregada'
ORDER_STATUS_CANCELLED = 'Cancelada'

ORDER_STATUS_CHOICES = (
    (ORDER_STATUS_PENDING, 'Pendiente'),
    (ORDER_STATUS_CONFIRMED, 'Confirmada'),
    (ORDER_STATUS_SHIPPED, 'Enviada'),
    (ORDER_STATUS_DELIVERED, 'Entregada'),
    (ORDER_STATUS_CANCELLED, 'Cancelada'),
)

# Métodos de pago
PAYMENT_METHOD_CASH = 'Efectivo'
PAYMENT_METHOD_CARD = 'Tarjeta'
PAYMENT_METHOD_TRANSFER = 'Transferencia'
PAYMENT_METHOD_CHECK = 'Cheque'

PAYMENT_METHOD_CHOICES = (
    (PAYMENT_METHOD_CASH, 'Efectivo'),
    (PAYMENT_METHOD_CARD, 'Tarjeta'),
    (PAYMENT_METHOD_TRANSFER, 'Transferencia'),
    (PAYMENT_METHOD_CHECK, 'Cheque'),
)

# Estados de pago
PAYMENT_STATUS_PENDING = 'Pendiente'
PAYMENT_STATUS_COMPLETED = 'Completado'
PAYMENT_STATUS_CANCELLED = 'Cancelado'

PAYMENT_STATUS_CHOICES = (
    (PAYMENT_STATUS_PENDING, 'Pendiente'),
    (PAYMENT_STATUS_COMPLETED, 'Completado'),
    (PAYMENT_STATUS_CANCELLED, 'Cancelado'),
)
