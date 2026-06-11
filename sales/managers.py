"""
Managers personalizados para el módulo de ventas
"""

from django.db import models
from django.db.models import Q, Sum, F


class OrderManager(models.Manager):
    """Manager personalizado para el modelo Order"""
    
    def pending(self):
        """Obtiene órdenes pendientes"""
        return self.filter(status='Pendiente')
    
    def paid(self):
        """Obtiene órdenes pagadas"""
        return self.filter(payment_status='Completado')
    
    def unpaid(self):
        """Obtiene órdenes sin pagar"""
        return self.exclude(payment_status='Completado')
    
    def recent(self, days=30):
        """Obtiene órdenes recientes"""
        from django.utils import timezone
        from datetime import timedelta
        
        since = timezone.now() - timedelta(days=days)
        return self.filter(created_at__gte=since)


class PaymentManager(models.Manager):
    """Manager personalizado para el modelo Payment"""
    
    def by_method(self, method):
        """Obtiene pagos de un método específico"""
        return self.filter(payment_method=method)
    
    def recent(self, days=30):
        """Obtiene pagos recientes"""
        from django.utils import timezone
        from datetime import timedelta
        
        since = timezone.now() - timedelta(days=days)
        return self.filter(date__gte=since)
