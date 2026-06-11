"""
Mixins personalizados para vistas de Django
"""

from django.shortcuts import redirect
from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponseForbidden


class AdminRequiredMixin(AccessMixin):
    """
    Mixin que verifica si el usuario es administrador
    """
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        
        is_admin = request.user.is_superuser or (
            hasattr(request.user, 'role') and request.user.role == 'ADMIN'
        )
        
        if not is_admin:
            return HttpResponseForbidden('Acceso denegado')
        
        return super().dispatch(request, *args, **kwargs)


class ProductionStaffMixin(AccessMixin):
    """
    Mixin que verifica si el usuario es parte del equipo de producción
    """
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        
        production_roles = ['PRODUCTION', 'PACKAGING', 'CUT', 'DESIGN', 'ADMIN']
        is_production = (
            request.user.is_superuser or
            (hasattr(request.user, 'role') and request.user.role in production_roles)
        )
        
        if not is_production:
            return HttpResponseForbidden('Acceso denegado')
        
        return super().dispatch(request, *args, **kwargs)


class DateFilterMixin:
    """
    Mixin que agrega filtrado por fecha a las vistas
    """
    
    def get_date_range(self):
        """Obtiene el rango de fechas del request"""
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        
        return {
            'start_date': start_date,
            'end_date': end_date
        }
