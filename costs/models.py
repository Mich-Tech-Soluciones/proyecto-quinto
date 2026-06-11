"""
Modelos para el módulo de costos
"""
from django.db import models
from sales.models import Order


class Cost(models.Model):
    """
    Modelo que registra los costos asociados a órdenes de producción.
    
    Atributos:
        order (ForeignKey): Orden relacionada al costo
        description (CharField): Descripción del costo
        amount (DecimalField): Monto del costo
        date (DateField): Fecha del registro del costo
    """
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        verbose_name="Pedido Relacionado",
        null=True,
        blank=True,
        related_name='costs'
    )
    description = models.CharField(max_length=255, verbose_name="Descripción del Costo")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Monto ($)")
    date = models.DateField(auto_now_add=True, verbose_name="Fecha")

    def __str__(self):
        return f"{self.description} - ${self.amount}"

    class Meta:
        verbose_name = "Costo"
        verbose_name_plural = "Costos"
        ordering = ['-date']
