"""
Señales (Signals) personalizadas para el proyecto
"""

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender='inventory.Product')
def product_saved(sender, instance, created, **kwargs):
    """
    Signal que se ejecuta cuando se guarda un producto
    """
    if created:
        logger.info(f"Nuevo producto creado: {instance.name}")
    else:
        logger.info(f"Producto actualizado: {instance.name}")


@receiver(post_save, sender='sales.Order')
def order_created(sender, instance, created, **kwargs):
    """
    Signal que se ejecuta cuando se crea una nueva orden
    """
    if created:
        logger.info(f"Nueva orden creada: #{instance.id} - {instance.customer_name}")
        # Aquí se podría enviar un email de confirmación
        try:
            if instance.customer_email:
                send_order_confirmation_email(instance)
        except Exception as e:
            logger.error(f"Error enviando email: {e}")


@receiver(post_save, sender='sales.Payment')
def payment_recorded(sender, instance, created, **kwargs):
    """
    Signal que se ejecuta cuando se registra un pago
    """
    if created:
        logger.info(f"Pago registrado: ${instance.amount} para orden #{instance.order.id}")


def send_order_confirmation_email(order):
    """
    Envía email de confirmación de orden
    """
    subject = f"Confirmación de Orden #{order.id}"
    message = f"Tu orden #{order.id} ha sido confirmada. Total: ${order.total}"
    
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [order.customer_email],
            fail_silently=False,
        )
        logger.info(f"Email de confirmación enviado a {order.customer_email}")
    except Exception as e:
        logger.error(f"Error al enviar email: {e}")
