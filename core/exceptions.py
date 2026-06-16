"""
Excepciones personalizadas para el proyecto
"""


class ATSException(Exception):
    """Excepción base para el proyecto"""
    pass


class InvalidProductError(ATSException):
    """Se lanza cuando hay un error con un producto"""
    pass


class InsufficientStockError(ATSException):
    """Se lanza cuando no hay suficiente stock"""
    pass


class InvalidOrderError(ATSException):
    """Se lanza cuando hay un error con una orden"""
    pass


class PaymentError(ATSException):
    """Se lanza cuando hay un error en el pago"""
    pass


class InvalidProductionStatusError(ATSException):
    """Se lanza cuando hay un error con el estado de producción"""
    pass
