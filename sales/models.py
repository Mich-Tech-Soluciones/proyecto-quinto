"""
Modelos para el módulo de ventas
"""
from decimal import Decimal

from django.db import models
from django.conf import settings
from inventory.models import Product


class Order(models.Model):
    """
    Modelo que representa una orden de venta.
    
    Atributos:
        customer_name (CharField): Nombre del cliente
        customer_email (EmailField): Email del cliente
        customer_phone (CharField): Teléfono del cliente
        company (CharField): Nombre de la empresa del cliente
        total (DecimalField): Total de la orden
        payment_method (CharField): Método de pago
        payment_status (CharField): Estado del pago
        status (CharField): Estado de la orden
        notes (TextField): Notas sobre el pedido
        technical_specs (TextField): Especificaciones técnicas
        design_image (ImageField): Imagen del diseño
        created_at (DateTimeField): Fecha de creación
        user (ForeignKey): Usuario que creó la orden
    """
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

    class Meta:
        verbose_name = "Orden de Venta"
        verbose_name_plural = "Órdenes de Venta"
        ordering = ['-created_at']

    @property
    def paid_amount(self):
        """Calcula el monto total pagado"""
        return sum((payment.amount for payment in self.payments.all()), Decimal('0.00'))
        
    @property
    def balance(self):
        """Calcula el saldo pendiente"""
        return Decimal(self.total) - self.paid_amount


class OrderDetail(models.Model):
    """
    Modelo que representa los detalles de una línea de orden.
    
    Atributos:
        order (ForeignKey): Orden relacionada
        product (ForeignKey): Producto pedido
        custom_name (CharField): Nombre personalizado del producto
        size (CharField): Talla o tamaño
        quantity (PositiveIntegerField): Cantidad
        unit_price (DecimalField): Precio unitario
        unit_cost (DecimalField): Costo unitario
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='details')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    custom_name = models.CharField(max_length=255, blank=True, null=True)
    size = models.CharField(max_length=20, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        verbose_name = "Detalle de Orden"
        verbose_name_plural = "Detalles de Orden"
        ordering = ['order', 'id']

    @property
    def subtotal(self):
        """Calcula el subtotal de la línea"""
        return self.quantity * self.unit_price

    def __str__(self):
        product_name = self.product.name if self.product else 'Producto eliminado'
        return f"{self.order.id} - {self.custom_name or product_name}"


class Payment(models.Model):
    """
    Modelo que registra los pagos realizados en una orden.
    
    Atributos:
        order (ForeignKey): Orden relacionada
        amount (DecimalField): Monto del pago
        payment_method (CharField): Método de pago utilizado
        note (CharField): Nota sobre el pago
        date (DateTimeField): Fecha del pago
        user (ForeignKey): Usuario que registró el pago
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    note = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"
        ordering = ['-date']

    def __str__(self):
        return f"Abono ${self.amount} - {self.order.id}"
