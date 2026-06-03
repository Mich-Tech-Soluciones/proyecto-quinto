from django.db import models
from django.conf import settings
from inventory.models import Product

class Order(models.Model):
    STATUS_CHOICES = (
        ('Pendiente', 'Pendiente'),
        ('Enviado', 'Enviado'),
        ('Pagado', 'Pagado'),
    )
    PAYMENT_STATUS_CHOICES = (
        ('Pendiente', 'Pendiente'),
        ('Parcial', 'Parcial'),
        ('Completado', 'Completado'),
    )

    customer_name = models.CharField(max_length=200, verbose_name="Nombre del Cliente")
    customer_email = models.EmailField(blank=True, null=True, verbose_name="Email")
    customer_phone = models.CharField(max_length=50, blank=True, null=True, verbose_name="Teléfono")
    company = models.CharField(max_length=200, blank=True, null=True, verbose_name="Empresa")
    
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_method = models.CharField(max_length=50, default="Efectivo")
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='Pendiente')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pendiente')
    
    notes = models.TextField(blank=True, null=True, verbose_name="Notas del Pedido")
    technical_specs = models.TextField(blank=True, null=True, verbose_name="Especificaciones Técnicas")
    design_image = models.ImageField(upload_to='designs/', null=True, blank=True, verbose_name="Diseño Adjunto")
    
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Pedido #{self.id} - {self.customer_name}"

    @property
    def paid_amount(self):
        return sum(payment.amount for payment in self.payments.all())
        
    @property
    def balance(self):
        return self.total - self.paid_amount

class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='details')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    custom_name = models.CharField(max_length=255, blank=True, null=True)
    size = models.CharField(max_length=20, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    @property
    def subtotal(self):
        return self.quantity * self.unit_price

    def __str__(self):
        return f"{self.order.id} - {self.custom_name or self.product.name}"

class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    note = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Abono ${self.amount} - {self.order.id}"
