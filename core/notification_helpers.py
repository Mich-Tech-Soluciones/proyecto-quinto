"""
Helpers para notificaciones
"""

from django.contrib.messages import add_message
from django.contrib.messages.constants import SUCCESS, ERROR, WARNING, INFO


def notify_success(request, message):
    """Agrega notificación de éxito"""
    add_message(request, SUCCESS, message)


def notify_error(request, message):
    """Agrega notificación de error"""
    add_message(request, ERROR, message)


def notify_warning(request, message):
    """Agrega notificación de advertencia"""
    add_message(request, WARNING, message)


def notify_info(request, message):
    """Agrega notificación de información"""
    add_message(request, INFO, message)


class NotificationSystem:
    """Sistema de notificaciones"""
    
    def __init__(self, request):
        self.request = request
    
    def success(self, message, extra_tags=''):
        """Notificación de éxito"""
        add_message(self.request, SUCCESS, message, extra_tags=extra_tags)
    
    def error(self, message, extra_tags=''):
        """Notificación de error"""
        add_message(self.request, ERROR, message, extra_tags=extra_tags)
    
    def warning(self, message, extra_tags=''):
        """Notificación de advertencia"""
        add_message(self.request, WARNING, message, extra_tags=extra_tags)
    
    def info(self, message, extra_tags=''):
        """Notificación de información"""
        add_message(self.request, INFO, message, extra_tags=extra_tags)


# Plantillas de mensajes predefinidos
MESSAGE_TEMPLATES = {
    'created': '{model} creado exitosamente',
    'updated': '{model} actualizado exitosamente',
    'deleted': '{model} eliminado exitosamente',
    'error': 'Error procesando {model}',
    'not_found': '{model} no encontrado',
    'unauthorized': 'No tiene permiso para acceder a {resource}',
    'low_stock': 'Alerta: {product} tiene bajo stock',
    'order_created': 'Orden #{order_id} creada exitosamente',
    'payment_received': 'Pago de ${amount} registrado para orden #{order_id}',
}


def get_notification_message(template_key, **kwargs):
    """
    Obtiene un mensaje de notificación predefinido
    
    Args:
        template_key: Clave de la plantilla
        **kwargs: Variables para formatear
    
    Returns:
        str: Mensaje formateado
    """
    template = MESSAGE_TEMPLATES.get(template_key, '')
    return template.format(**kwargs)
