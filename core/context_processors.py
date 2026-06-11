"""
Contextos personalizados para templates
"""

from django.conf import settings


def site_context(request):
    """
    Contexto global para todas las templates
    """
    return {
        'site_name': 'Kaza',
        'site_title': 'Kaza - Sistema de Gestión',
        'debug': settings.DEBUG,
        'user': request.user,
    }


def navigation_context(request):
    """
    Contexto para navegación
    """
    return {
        'navigation_items': get_navigation_items(request.user),
    }


def get_navigation_items(user):
    """
    Obtiene los items de navegación según el rol del usuario
    """
    items = []
    
    # Items básicos
    items.append({
        'title': 'Dashboard',
        'url': '/',
        'icon': 'bi-house',
    })
    
    # Items por rol
    if user.is_authenticated:
        if user.is_superuser or (hasattr(user, 'role') and user.role == 'ADMIN'):
            items.extend([
                {'title': 'Usuarios', 'url': '/users/', 'icon': 'bi-people'},
                {'title': 'Inventario', 'url': '/inventory/', 'icon': 'bi-boxes'},
                {'title': 'Ventas', 'url': '/sales/', 'icon': 'bi-cart'},
                {'title': 'Producción', 'url': '/production/', 'icon': 'bi-hammer'},
                {'title': 'Costos', 'url': '/costs/', 'icon': 'bi-calculator'},
            ])
        elif hasattr(user, 'role'):
            if user.role in ['PRODUCTION', 'PACKAGING', 'CUT', 'DESIGN']:
                items.extend([
                    {'title': 'Producción', 'url': '/production/', 'icon': 'bi-hammer'},
                    {'title': 'Órdenes', 'url': '/sales/', 'icon': 'bi-list'},
                ])
    
    return items
