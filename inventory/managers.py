"""
Managers personalizados para el módulo de inventario
"""

from django.db import models


class ProductManager(models.Manager):
    """Manager personalizado para el modelo Product"""
    
    def featured(self):
        """Obtiene todos los productos destacados"""
        return self.filter(featured=True)
    
    def with_low_stock(self, threshold=5):
        """Obtiene productos con stock bajo"""
        return self.filter(stock__lte=threshold)
    
    def available(self):
        """Obtiene productos disponibles"""
        return self.filter(stock__gt=0)
    
    def by_catalog(self, catalog_id):
        """Obtiene productos de un catálogo específico"""
        return self.filter(catalog_id=catalog_id)


class CatalogManager(models.Manager):
    """Manager personalizado para el modelo Catalog"""
    
    def with_products_count(self):
        """Obtiene catálogos con conteo de productos"""
        from django.db.models import Count
        return self.annotate(product_count=Count('categories__categories__product'))
