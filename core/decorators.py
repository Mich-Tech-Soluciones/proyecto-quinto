"""
Decoradores personalizados para el proyecto
"""

from functools import wraps
from django.http import HttpResponseForbidden


def admin_required(view_func):
    """
    Decorador que verifica si el usuario es administrador
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden('No autenticado')
        
        # Verificar si es superusuario o tiene rol ADMIN
        is_admin = request.user.is_superuser or (
            hasattr(request.user, 'role') and request.user.role == 'ADMIN'
        )
        
        if not is_admin:
            return HttpResponseForbidden('Acceso denegado')
        
        return view_func(request, *args, **kwargs)
    
    return wrapper


def production_staff_required(view_func):
    """
    Decorador que verifica si el usuario es parte del equipo de producción
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden('No autenticado')
        
        production_roles = ['PRODUCTION', 'PACKAGING', 'CUT', 'DESIGN', 'ADMIN']
        is_production_staff = (
            request.user.is_superuser or
            (hasattr(request.user, 'role') and request.user.role in production_roles)
        )
        
        if not is_production_staff:
            return HttpResponseForbidden('Acceso denegado')
        
        return view_func(request, *args, **kwargs)
    
    return wrapper
