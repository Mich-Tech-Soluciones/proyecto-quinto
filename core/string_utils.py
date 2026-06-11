"""
Utilidades para manipulación de strings
"""

import re
from django.utils.text import slugify


def truncate_string(text, max_length=50, suffix='...'):
    """
    Trunca un string a una longitud máxima
    
    Args:
        text: Texto a truncar
        max_length: Longitud máxima
        suffix: Sufijo a agregar
    
    Returns:
        str: Texto truncado
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def capitalize_words(text):
    """
    Capitaliza cada palabra en un string
    
    Args:
        text: Texto a capitalizar
    
    Returns:
        str: Texto capitalizado
    """
    return ' '.join(word.capitalize() for word in text.split())


def normalize_whitespace(text):
    """
    Normaliza espacios en blanco
    
    Args:
        text: Texto a normalizar
    
    Returns:
        str: Texto normalizado
    """
    return ' '.join(text.split())


def remove_accents(text):
    """
    Elimina acentos de un texto
    
    Args:
        text: Texto con acentos
    
    Returns:
        str: Texto sin acentos
    """
    import unicodedata
    return ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    )


def generate_slug(text):
    """
    Genera un slug a partir de un texto
    
    Args:
        text: Texto base
    
    Returns:
        str: Slug generado
    """
    return slugify(remove_accents(text))


def is_valid_email(email):
    """
    Valida si un email es válido
    
    Args:
        email: Email a validar
    
    Returns:
        bool: True si es válido
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def is_valid_phone(phone):
    """
    Valida si un teléfono es válido
    
    Args:
        phone: Teléfono a validar
    
    Returns:
        bool: True si es válido
    """
    pattern = r'^\+?1?\d{9,15}$'
    clean_phone = phone.replace('-', '').replace(' ', '').replace('+', '').replace('(', '').replace(')', '')
    return re.match(pattern, clean_phone) is not None


def extract_numbers(text):
    """
    Extrae números de un texto
    
    Args:
        text: Texto a procesar
    
    Returns:
        list: Lista de números encontrados
    """
    return re.findall(r'\d+', text)


def mask_email(email):
    """
    Enmasca ra un email para privacidad
    
    Args:
        email: Email a enmascarar
    
    Returns:
        str: Email enmascarado
    """
    parts = email.split('@')
    if len(parts) != 2:
        return email
    
    user, domain = parts
    masked_user = user[0] + '*' * (len(user) - 2) + user[-1] if len(user) > 2 else user
    return f"{masked_user}@{domain}"
