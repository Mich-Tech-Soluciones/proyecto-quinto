from django.db import models
from django.conf import settings

class Catalog(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Nombre del Catálogo")
    icon = models.CharField(max_length=50, default="bi-folder", verbose_name="Icono")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Catálogo"
        verbose_name_plural = "Catálogos"

class Category(models.Model):
    catalog = models.ForeignKey(Catalog, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=100, verbose_name="Nombre de Categoría")

    def __str__(self):
        return f"{self.catalog.name} - {self.name}"

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        unique_together = ('catalog', 'name')

class Product(models.Model):
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

class ProductSize(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sizes')
    size = models.CharField(max_length=20, verbose_name="Talla")
    stock = models.PositiveIntegerField(default=0, verbose_name="Stock de Talla")

    def __str__(self):
        return f"{self.product.name} - {self.size}"

    class Meta:
        verbose_name = "Talla de Producto"
        verbose_name_plural = "Tallas de Producto"
        unique_together = ('product', 'size')

class Kardex(models.Model):
    MOVEMENT_CHOICES = (
        ('Entrada', 'Entrada'),
        ('Salida', 'Salida'),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
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
