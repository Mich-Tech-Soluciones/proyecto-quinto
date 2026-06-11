"""
Modelos para el módulo de inventario
"""
from django.db import models
from django.conf import settings


class Catalog(models.Model):
    """
    Modelo que representa un catálogo de productos.
    
    Atributos:
        name (CharField): Nombre único del catálogo
        icon (CharField): Icono del catálogo (Bootstrap Icons)
    """
    name = models.CharField(max_length=100, unique=True, verbose_name="Nombre del Catálogo")
    icon = models.CharField(max_length=50, default="bi-folder", verbose_name="Icono")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Catálogo"
        verbose_name_plural = "Catálogos"
        ordering = ['name']


class Category(models.Model):
    """
    Modelo que representa una categoría dentro de un catálogo.
    
    Atributos:
        catalog (ForeignKey): Catálogo al que pertenece
        name (CharField): Nombre de la categoría
    """
    catalog = models.ForeignKey(Catalog, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=100, verbose_name="Nombre de Categoría")

    def __str__(self):
        return f"{self.catalog.name} - {self.name}"

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        unique_together = ('catalog', 'name')
        ordering = ['catalog', 'name']


class Product(models.Model):
    """
    Modelo que representa un producto del inventario.
    
    Atributos:
        name (CharField): Nombre del producto
        description (TextField): Descripción detallada
        catalog (ForeignKey): Catálogo del producto
        category (ForeignKey): Categoría del producto
        price (DecimalField): Precio de venta
        cost (DecimalField): Costo de producción
        stock (PositiveIntegerField): Stock disponible global
        featured (BooleanField): Indica si está destacado
        image (ImageField): Imagen del producto
        created_at (DateTimeField): Fecha de creación
        updated_at (DateTimeField): Fecha de última actualización
    """
    name = models.CharField(max_length=200, verbose_name="Nombre del Producto")
    description = models.TextField(blank=True, verbose_name="Descripción")
    catalog = models.ForeignKey(Catalog, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio")
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Costo")
    stock = models.PositiveIntegerField(default=0, verbose_name="Stock Global")
    featured = models.BooleanField(default=False, verbose_name="Destacado")
    image = models.ImageField(upload_to='products/', null=True, blank=True, verbose_name="Imagen")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['-created_at', 'name']

    @property
    def profit_margin(self):
        """Calcula el margen de ganancia del producto"""
        if self.cost == 0:
            return 0
        return ((self.price - self.cost) / self.cost) * 100


class ProductSize(models.Model):
    """
    Modelo que representa las tallas disponibles de un producto.
    
    Atributos:
        product (ForeignKey): Producto al que pertenece la talla
        size (CharField): Tamaño o talla del producto
        stock (PositiveIntegerField): Stock disponible para esta talla
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sizes')
    size = models.CharField(max_length=20, verbose_name="Talla")
    stock = models.PositiveIntegerField(default=0, verbose_name="Stock de Talla")

    def __str__(self):
        return f"{self.product.name} - {self.size}"

    class Meta:
        verbose_name = "Talla de Producto"
        verbose_name_plural = "Tallas de Producto"
        unique_together = ('product', 'size')
        ordering = ['product', 'size']


class Kardex(models.Model):
    """
    Modelo que registra todos los movimientos de inventario.
    
    Atributos:
        product (ForeignKey): Producto movido
        size (CharField): Talla del producto (opcional)
        movement_type (CharField): Tipo de movimiento (Entrada/Salida)
        quantity (PositiveIntegerField): Cantidad del movimiento
        prev_stock (PositiveIntegerField): Stock anterior
        new_stock (PositiveIntegerField): Stock actualizado
        reason (CharField): Razón del movimiento
        user (ForeignKey): Usuario que realizó el movimiento
        date (DateTimeField): Fecha del movimiento
    """
    MOVEMENT_CHOICES = (
        ('Entrada', 'Entrada'),
        ('Salida', 'Salida'),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='movements')
    size = models.CharField(max_length=20, blank=True, null=True)
    movement_type = models.CharField(max_length=10, choices=MOVEMENT_CHOICES)
    quantity = models.PositiveIntegerField()
    prev_stock = models.PositiveIntegerField()
    new_stock = models.PositiveIntegerField()
    reason = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.movement_type} - {self.product.name} ({self.quantity})"

    class Meta:
        verbose_name = "Movimiento de Kardex"
        verbose_name_plural = "Movimientos de Kardex"
        ordering = ['-date']

