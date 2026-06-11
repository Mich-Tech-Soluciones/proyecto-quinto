"""
Helpers para manejo de emails
"""

from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
import logging

logger = logging.getLogger(__name__)


def send_simple_email(subject, message, recipient_list, fail_silently=False):
    """
    Envía un email simple
    
    Args:
        subject: Asunto del email
        message: Mensaje del email
        recipient_list: Lista de destinatarios
        fail_silently: Si debe fallar silenciosamente
    
    Returns:
        int: Número de emails enviados
    """
    try:
        return send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            recipient_list,
            fail_silently=fail_silently,
        )
    except Exception as e:
        logger.error(f"Error enviando email: {e}")
        return 0


def send_email_with_template(subject, template_name, context, recipient_list):
    """
    Envía un email usando una template
    
    Args:
        subject: Asunto del email
        template_name: Nombre de la template
        context: Contexto para la template
        recipient_list: Lista de destinatarios
    
    Returns:
        int: Número de emails enviados
    """
    try:
        html_message = render_to_string(template_name, context)
        
        email = EmailMultiAlternatives(
            subject,
            "Email HTML",
            settings.DEFAULT_FROM_EMAIL,
            recipient_list,
        )
        email.attach_alternative(html_message, "text/html")
        email.send()
        
        logger.info(f"Email enviado a {recipient_list}")
        return 1
    except Exception as e:
        logger.error(f"Error enviando email con template: {e}")
        return 0


def send_order_confirmation_email(order):
    """
    Envía email de confirmación de orden
    
    Args:
        order: Instancia de Order
    
    Returns:
        bool: True si se envió correctamente
    """
    if not order.customer_email:
        logger.warning(f"Orden {order.id} sin email de cliente")
        return False
    
    subject = f"Confirmación de Orden #{order.id}"
    context = {
        'order': order,
        'total': order.total,
        'customer_name': order.customer_name,
    }
    
    return send_email_with_template(
        subject,
        'emails/order_confirmation.html',
        context,
        [order.customer_email]
    ) == 1
