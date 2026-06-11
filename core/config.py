"""
Configuración de desarrollo y utilidades adicionales
"""

import os
from pathlib import Path

# Información del proyecto
PROJECT_NAME = 'Kaza'
PROJECT_DESCRIPTION = 'Sistema de Gestión de Producción y Ventas'
PROJECT_VERSION = '1.0.0'

# Directorios
BASE_DIR = Path(__file__).resolve().parent.parent
LOGS_DIR = os.path.join(BASE_DIR, 'logs')
MEDIA_DIR = os.path.join(BASE_DIR, 'media')
STATIC_DIR = os.path.join(BASE_DIR, 'static')

# Crear directorios si no existen
for directory in [LOGS_DIR, MEDIA_DIR]:
    os.makedirs(directory, exist_ok=True)

# Configuración de desarrollo
DEVELOPMENT_MODE = os.environ.get('DEBUG', 'True') == 'True'

# Aplicaciones instaladas
INSTALLED_APPS_CORE = [
    'core',
    'users',
    'inventory',
    'production',
    'sales',
    'costs',
    'dashboard',
]

# Middlewares personalizados
MIDDLEWARE_CUSTOM = [
    'core.middleware.AuthenticationMiddleware',
    'core.middleware.LoggingMiddleware',
]

# Context Processors personalizados
CONTEXT_PROCESSORS_CUSTOM = [
    'core.context_processors.site_context',
    'core.context_processors.navigation_context',
]

# Configuraciones de caché (ejemplo)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'kaza-cache',
    }
}

# Configuración de sesión
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 86400  # 24 horas
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = False  # Cambiar a True en producción

# Configuración de seguridad básica
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_SECURITY_POLICY = {
    'default-src': ("'self'",),
    'script-src': ("'self'", "'unsafe-inline'"),
    'style-src': ("'self'", "'unsafe-inline'"),
}

# Datos de ejemplo para desarrollo
DEMO_DATA = {
    'admin_username': 'admin',
    'admin_email': 'admin@kaza.local',
    'demo_users': [
        {'username': 'designer', 'role': 'DESIGN'},
        {'username': 'cutter', 'role': 'CUT'},
        {'username': 'producer', 'role': 'PRODUCTION'},
        {'username': 'packer', 'role': 'PACKAGING'},
    ]
}

# Configuración de reportes
REPORT_SETTINGS = {
    'date_format': 'Y-m-d',
    'currency_symbol': '$',
    'decimal_separator': '.',
    'thousands_separator': ',',
}

# Permisos por defecto
DEFAULT_PERMISSIONS = {
    'ADMIN': ['*'],  # Acceso total
    'DESIGN': ['inventory:view', 'inventory:add', 'production:view', 'production:edit'],
    'CUT': ['production:view', 'production:edit'],
    'PRODUCTION': ['production:view', 'production:edit', 'inventory:view'],
    'PACKAGING': ['production:view', 'inventory:view'],
}

def get_development_settings():
    """Retorna configuraciones de desarrollo"""
    return {
        'DEBUG': True,
        'ALLOWED_HOSTS': ['localhost', '127.0.0.1'],
        'LOG_LEVEL': 'DEBUG',
    }


def get_production_settings():
    """Retorna configuraciones de producción"""
    return {
        'DEBUG': False,
        'ALLOWED_HOSTS': ['kaza.example.com'],
        'LOG_LEVEL': 'WARNING',
        'SECURE_SSL_REDIRECT': True,
        'SESSION_COOKIE_SECURE': True,
        'CSRF_COOKIE_SECURE': True,
    }
