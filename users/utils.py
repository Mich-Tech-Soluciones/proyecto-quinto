"""
Utilidades y funciones auxiliares para el módulo de usuarios
"""

from django.contrib.auth import get_user_model

User = get_user_model()


def get_user_role_display(user):
    """
    Obtiene la representación en texto del rol del usuario
    
    Args:
        user: Instancia de usuario
    
    Returns:
        str: Descripción del rol del usuario
    """
    return user.get_role_display() if hasattr(user, 'get_role_display') else 'N/A'


def is_admin_user(user):
    """
    Verifica si el usuario tiene rol de administrador
    
    Args:
        user: Instancia de usuario
    
    Returns:
        bool: True si es administrador, False en caso contrario
    """
    if user.is_superuser:
        return True
    return user.role == 'ADMIN' if hasattr(user, 'role') else False


def get_users_by_role(role):
    """
    Obtiene todos los usuarios con un rol específico
    
    Args:
        role: Rol a buscar
    
    Returns:
        QuerySet: Usuarios con el rol especificado
    """
    return User.objects.filter(role=role)
