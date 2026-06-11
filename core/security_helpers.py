"""
Helpers para seguridad del proyecto
"""

import hashlib
import secrets
from django.contrib.auth.hashers import make_password, check_password


def generate_token(length=32):
    """
    Genera un token seguro aleatorio
    
    Args:
        length: Longitud del token
    
    Returns:
        str: Token aleatorio
    """
    return secrets.token_urlsafe(length)


def hash_password(password):
    """
    Hashea una contraseña
    
    Args:
        password: Contraseña a hashear
    
    Returns:
        str: Contraseña hasheada
    """
    return make_password(password)


def verify_password(password, hashed):
    """
    Verifica una contraseña contra su hash
    
    Args:
        password: Contraseña a verificar
        hashed: Hash de la contraseña
    
    Returns:
        bool: True si coinciden
    """
    return check_password(password, hashed)


def hash_string(text):
    """
    Hashea una cadena de texto
    
    Args:
        text: Texto a hashear
    
    Returns:
        str: Hash SHA256
    """
    return hashlib.sha256(text.encode()).hexdigest()


def is_strong_password(password):
    """
    Verifica si una contraseña es fuerte
    
    Args:
        password: Contraseña a verificar
    
    Returns:
        dict: Resultado de la verificación
    """
    requirements = {
        'min_length': len(password) >= 8,
        'has_upper': any(c.isupper() for c in password),
        'has_lower': any(c.islower() for c in password),
        'has_digit': any(c.isdigit() for c in password),
        'has_special': any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password),
    }
    
    return {
        'is_strong': all(requirements.values()),
        'requirements': requirements,
    }


SANITIZATION_RULES = {
    'remove_tags': {
        'patterns': ['<script>', '</script>', '<iframe>', '</iframe>'],
        'description': 'Elimina etiquetas peligrosas',
    },
    'escape_quotes': {
        'patterns': ["'", '"'],
        'description': 'Escapa comillas',
    },
}


def sanitize_input(text, rules='remove_tags'):
    """
    Sanitiza entrada de usuario
    
    Args:
        text: Texto a sanitizar
        rules: Reglas a aplicar
    
    Returns:
        str: Texto sanitizado
    """
    if not text:
        return text
    
    if rules == 'remove_tags':
        for pattern in SANITIZATION_RULES['remove_tags']['patterns']:
            text = text.replace(pattern, '')
    
    return text
