"""
Constantes para la aplicación de inventario
"""

# Movimientos de Kardex
MOVEMENT_TYPE_ENTRADA = 'Entrada'
MOVEMENT_TYPE_SALIDA = 'Salida'

MOVEMENT_CHOICES = (
    (MOVEMENT_TYPE_ENTRADA, 'Entrada'),
    (MOVEMENT_TYPE_SALIDA, 'Salida'),
)

# Valores por defecto
DEFAULT_PRODUCT_COST = 0.00
DEFAULT_PRODUCT_STOCK = 0
DEFAULT_ICON = 'bi-folder'

# Límites
MIN_STOCK_WARNING = 5
MAX_PRODUCT_NAME_LENGTH = 200
MAX_CATEGORY_NAME_LENGTH = 100
