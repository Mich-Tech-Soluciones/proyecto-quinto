"""
Helpers para documentación de API
"""


class APIEndpoint:
    """Clase para documentar endpoints de API"""
    
    def __init__(self, path, method, description, parameters=None, response=None):
        self.path = path
        self.method = method
        self.description = description
        self.parameters = parameters or []
        self.response = response or {}
    
    def to_dict(self):
        """Convierte el endpoint a diccionario"""
        return {
            'path': self.path,
            'method': self.method,
            'description': self.description,
            'parameters': self.parameters,
            'response': self.response,
        }


# Documentación de API endpoints
API_ENDPOINTS = [
    APIEndpoint(
        path='/api/products/',
        method='GET',
        description='Obtiene lista de productos',
        parameters=[
            {'name': 'page', 'type': 'integer', 'description': 'Número de página'},
            {'name': 'catalog', 'type': 'integer', 'description': 'ID del catálogo'},
        ],
    ),
    APIEndpoint(
        path='/api/orders/',
        method='GET',
        description='Obtiene lista de órdenes',
        parameters=[
            {'name': 'status', 'type': 'string', 'description': 'Estado de la orden'},
        ],
    ),
    APIEndpoint(
        path='/api/production/',
        method='GET',
        description='Obtiene hojas de producción',
    ),
]


def get_api_documentation():
    """Retorna la documentación de la API"""
    return {
        'endpoints': [ep.to_dict() for ep in API_ENDPOINTS],
        'base_url': '/api/v1',
        'authentication': 'Token',
    }


def document_endpoint(path, method, description):
    """
    Decorador para documentar endpoints
    
    Args:
        path: Ruta del endpoint
        method: Método HTTP
        description: Descripción del endpoint
    """
    def decorator(func):
        func._api_endpoint = APIEndpoint(path, method, description)
        return func
    return decorator
