from django.db import models
from sales.models import Order

class ProductionSheet(models.Model):
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
    
    # Signatures/Approvals could be logged here or in a separate model
    designed_by = models.CharField(max_length=100, blank=True, null=True)
    produced_by = models.CharField(max_length=100, blank=True, null=True)
    qc_by = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Hoja Producción #{self.id} (Pedido #{self.order.id})"
