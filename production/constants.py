"""
Constantes para la aplicación de producción
"""

# Estados de producción
STATUS_PENDING = 'Pendiente'
STATUS_IN_PROGRESS = 'En Proceso'
STATUS_COMPLETED = 'Completado'
STATUS_CANCELLED = 'Cancelado'

STATUS_CHOICES = (
    (STATUS_PENDING, 'Pendiente'),
    (STATUS_IN_PROGRESS, 'En Proceso'),
    (STATUS_COMPLETED, 'Completado'),
    (STATUS_CANCELLED, 'Cancelado'),
)

# Prioridades
PRIORITY_LOW = 'Baja'
PRIORITY_MEDIUM = 'Media'
PRIORITY_HIGH = 'Alta'
PRIORITY_URGENT = 'Urgente'

PRIORITY_CHOICES = (
    (PRIORITY_LOW, 'Baja'),
    (PRIORITY_MEDIUM, 'Media'),
    (PRIORITY_HIGH, 'Alta'),
    (PRIORITY_URGENT, 'Urgente'),
)
