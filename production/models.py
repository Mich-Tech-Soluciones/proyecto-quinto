"""
Modelos para el módulo de producción
"""
from django.db import models
from sales.models import Order


class ProductionSheet(models.Model):
    """
    Modelo que representa una hoja de producción asociada a una orden.
    
    Atributos:
        order (OneToOneField): Orden de venta relacionada
        status (CharField): Estado actual de la producción
        created_at (DateTimeField): Fecha de creación
        updated_at (DateTimeField): Fecha de última actualización
        designed_by (CharField): Nombre del diseñador
        produced_by (CharField): Nombre del productor
        qc_by (CharField): Nombre del responsable de control de calidad
    """
    STATUS_CHOICES = (
        ('Pendiente', 'Pendiente'),
        ('En Corte', 'En Corte'),
        ('En Costura', 'En Costura'),
        ('Control Calidad', 'Control Calidad'),
        ('Completado', 'Completado'),
    )

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='production_sheet')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pendiente')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Signatures/Approvals
    designed_by = models.CharField(max_length=100, blank=True, null=True, verbose_name="Diseñado por")
    produced_by = models.CharField(max_length=100, blank=True, null=True, verbose_name="Producido por")
    qc_by = models.CharField(max_length=100, blank=True, null=True, verbose_name="Control de calidad por")

    def __str__(self):
        return f"Hoja Producción #{self.id} (Pedido #{self.order.id})"

    class Meta:
        verbose_name = "Hoja de Producción"
        verbose_name_plural = "Hojas de Producción"
        ordering = ['-created_at']
