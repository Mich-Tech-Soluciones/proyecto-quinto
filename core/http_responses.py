"""
Helpers para respuestas HTTP personalizadas
"""

from django.http import JsonResponse, HttpResponse
from django.template.response import TemplateResponse
import json


def json_response(data, status_code=200, **kwargs):
    """
    Retorna una respuesta JSON
    
    Args:
        data: Datos a serializar
        status_code: Código HTTP
        **kwargs: Argumentos adicionales
    
    Returns:
        JsonResponse: Respuesta JSON
    """
    return JsonResponse(data, status=status_code, **kwargs)


def json_error_response(message, error_code=None, status_code=400):
    """
    Retorna una respuesta de error JSON
    
    Args:
        message: Mensaje de error
        error_code: Código de error
        status_code: Código HTTP
    
    Returns:
        JsonResponse: Respuesta de error JSON
    """
    data = {
        'success': False,
        'error': message,
    }
    
    if error_code:
        data['error_code'] = error_code
    
    return json_response(data, status_code)


def json_success_response(data=None, message='Éxito', status_code=200):
    """
    Retorna una respuesta de éxito JSON
    
    Args:
        data: Datos adicionales
        message: Mensaje de éxito
        status_code: Código HTTP
    
    Returns:
        JsonResponse: Respuesta de éxito JSON
    """
    response = {
        'success': True,
        'message': message,
    }
    
    if data:
        response['data'] = data
    
    return json_response(response, status_code)


def paginated_response(items, page_number, total_pages, status_code=200):
    """
    Retorna una respuesta paginada JSON
    
    Args:
        items: Items de la página
        page_number: Número de página
        total_pages: Total de páginas
        status_code: Código HTTP
    
    Returns:
        JsonResponse: Respuesta paginada
    """
    data = {
        'success': True,
        'data': items,
        'pagination': {
            'page': page_number,
            'total_pages': total_pages,
            'items_count': len(items),
        }
    }
    
    return json_response(data, status_code)


class APIResponse:
    """Clase para construir respuestas de API"""
    
    @staticmethod
    def success(data=None, message='Éxito', status_code=200):
        """Respuesta de éxito"""
        return json_success_response(data, message, status_code)
    
    @staticmethod
    def error(message, error_code=None, status_code=400):
        """Respuesta de error"""
        return json_error_response(message, error_code, status_code)
    
    @staticmethod
    def created(data, message='Creado exitosamente'):
        """Respuesta de recurso creado"""
        return json_success_response(data, message, 201)
    
    @staticmethod
    def not_found(message='Recurso no encontrado'):
        """Respuesta de recurso no encontrado"""
        return json_error_response(message, 'NOT_FOUND', 404)
    
    @staticmethod
    def unauthorized(message='No autorizado'):
        """Respuesta no autorizada"""
        return json_error_response(message, 'UNAUTHORIZED', 401)
    
    @staticmethod
    def forbidden(message='Acceso denegado'):
        """Respuesta acceso denegado"""
        return json_error_response(message, 'FORBIDDEN', 403)
    
    @staticmethod
    def paginated(items, page_number, total_pages):
        """Respuesta paginada"""
        return paginated_response(items, page_number, total_pages)
