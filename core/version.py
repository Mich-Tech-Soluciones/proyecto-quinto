"""
Información de versión del proyecto
"""

__version__ = "1.0.0"
__version_info__ = (1, 0, 0)

VERSION = __version__

def get_version():
    """Retorna la versión del proyecto"""
    return __version__


def get_version_tuple():
    """Retorna la versión como tupla"""
    return __version_info__


RELEASE_DATE = "2024-01-15"

CHANGELOG = {
    "1.0.0": {
        "date": "2024-01-15",
        "changes": [
            "Versión inicial del sistema",
            "Módulos de inventario, producción, ventas y costos",
            "Sistema de usuarios con roles",
            "Panel de control",
            "Generación de reportes",
        ]
    }
}


def get_changelog(version=None):
    """
    Retorna el changelog
    
    Args:
        version: Versión específica o None para todas
    
    Returns:
        dict: Información del changelog
    """
    if version:
        return CHANGELOG.get(version)
    return CHANGELOG
