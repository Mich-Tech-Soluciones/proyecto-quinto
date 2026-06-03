from django.db import models
from sales.models import Order

class Cost(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Pedido Relacionado", null=True, blank=True)
    description = models.CharField(max_length=255, verbose_name="Descripción del Costo")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Monto ($)")
    date = models.DateField(auto_now_add=True, verbose_name="Fecha")

    def __str__(self):
        return f"{self.description} - ${self.amount}"

    class Meta:
        verbose_name = "Costo"
        verbose_name_plural = "Costos"
