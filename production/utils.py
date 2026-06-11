"""
Utilidades y funciones auxiliares para el módulo de producción
"""

from .models import ProductionSheet


def get_production_sheet_status_color(status):
    """
    Obtiene el color asociado a un estado de producción para UI
    
    Args:
        status: Estado de la producción
    
    Returns:
        str: Código de color hexadecimal
    """
    status_colors = {
        'Pendiente': '#FFC107',
        'En Corte': '#2196F3',
        'En Costura': '#9C27B0',
        'Control Calidad': '#FF9800',
        'Completado': '#4CAF50',
    }
    return status_colors.get(status, '#757575')


def get_production_progress(production_sheet):
    """
    Calcula el progreso de una hoja de producción
    
    Args:
        production_sheet: Instancia de ProductionSheet
    
    Returns:
        dict: Información del progreso con porcentaje
    """
    status_progress = {
        'Pendiente': 0,
        'En Corte': 25,
        'En Costura': 50,
        'Control Calidad': 75,
        'Completado': 100,
    }
    
    progress = status_progress.get(production_sheet.status, 0)
    return {
        'progress': progress,
        'status': production_sheet.status,
        'remaining': 100 - progress
    }
