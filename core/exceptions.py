"""
Excepciones personalizadas para el proyecto
"""


class KazaException(Exception):
    """Excepción base para el proyecto"""
    pass


class InvalidProductError(KazaException):
    """Se lanza cuando hay un error con un producto"""
    pass


class InsufficientStockError(KazaException):
    """Se lanza cuando no hay suficiente stock"""
    pass


class InvalidOrderError(KazaException):
    """Se lanza cuando hay un error con una orden"""
    pass


class PaymentError(KazaException):
    """Se lanza cuando hay un error en el pago"""
    pass


class InvalidProductionStatusError(KazaException):
    """Se lanza cuando hay un error con el estado de producción"""
    pass
