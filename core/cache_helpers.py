"""
Helpers para manejo de caché
"""

from django.core.cache import cache
from django.views.decorators.cache import cache_page
from functools import wraps
import hashlib


def cache_key(prefix, *args, **kwargs):
    """
    Genera una clave de caché única
    
    Args:
        prefix: Prefijo de la clave
        *args: Argumentos
        **kwargs: Argumentos con nombre
    
    Returns:
        str: Clave de caché
    """
    key_data = f"{prefix}:{str(args)}:{str(sorted(kwargs.items()))}"
    hash_obj = hashlib.md5(key_data.encode())
    return f"ats:{hash_obj.hexdigest()}"


def get_or_cache(key, func, timeout=300):
    """
    Obtiene un valor del caché o lo calcula
    
    Args:
        key: Clave del caché
        func: Función a ejecutar si no está en caché
        timeout: Tiempo de expiración en segundos
    
    Returns:
        Valor del caché o resultado de la función
    """
    value = cache.get(key)
    if value is None:
        value = func()
        cache.set(key, value, timeout)
    return value


def clear_cache_pattern(pattern):
    """
    Limpia todas las claves del caché que coincidan con un patrón
    
    Args:
        pattern: Patrón de búsqueda
    """
    # Para Django con Redis backend
    try:
        cache.delete_pattern(f"ats:{pattern}*")
    except AttributeError:
        # Si no está disponible el método
        pass


def cache_model_list(model_class, timeout=300):
    """
    Cachea la lista de todos los objetos de un modelo
    
    Args:
        model_class: Clase del modelo
        timeout: Tiempo de expiración
    
    Returns:
        QuerySet del modelo
    """
    key = cache_key(f'{model_class.__name__}:list')
    
    def get_list():
        return list(model_class.objects.all())
    
    return get_or_cache(key, get_list, timeout)


def invalidate_model_cache(model_class):
    """
    Invalida el caché de un modelo
    
    Args:
        model_class: Clase del modelo
    """
    key = cache_key(f'{model_class.__name__}:list')
    cache.delete(key)
