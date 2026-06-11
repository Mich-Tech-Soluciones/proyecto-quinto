"""
Middleware personalizado para el proyecto
"""

from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseForbidden
import logging

logger = logging.getLogger(__name__)


class AuthenticationMiddleware(MiddlewareMixin):
    """
    Middleware que agrega información de autenticación al request
    """
    
    def process_request(self, request):
        """Agrega información del usuario al request"""
        if request.user.is_authenticated:
            request.user_role = getattr(request.user, 'role', 'GUEST')
            request.is_admin = request.user.is_superuser or request.user.role == 'ADMIN'
        else:
            request.user_role = 'GUEST'
            request.is_admin = False
        
        return None


class LoggingMiddleware(MiddlewareMixin):
    """
    Middleware que registra las peticiones HTTP
    """
    
    def process_request(self, request):
        """Registra información de la petición"""
        logger.info(f"REQUEST: {request.method} {request.path} - User: {request.user}")
        return None
    
    def process_response(self, request, response):
        """Registra información de la respuesta"""
        logger.info(f"RESPONSE: {request.method} {request.path} - Status: {response.status_code}")
        return response
