"""
Constantes para la aplicación de costos
"""

# Tipos de costos
COST_TYPE_MATERIAL = 'Material'
COST_TYPE_LABOR = 'Mano de Obra'
COST_TYPE_OVERHEAD = 'Gastos Generales'
COST_TYPE_OTHER = 'Otro'

COST_TYPE_CHOICES = (
    (COST_TYPE_MATERIAL, 'Material'),
    (COST_TYPE_LABOR, 'Mano de Obra'),
    (COST_TYPE_OVERHEAD, 'Gastos Generales'),
    (COST_TYPE_OTHER, 'Otro'),
)

# Unidades de medida
UNIT_KILOGRAMS = 'kg'
UNIT_METERS = 'm'
UNIT_HOURS = 'h'
UNIT_UNITS = 'unidad'

UNIT_CHOICES = (
    (UNIT_KILOGRAMS, 'Kilogramos'),
    (UNIT_METERS, 'Metros'),
    (UNIT_HOURS, 'Horas'),
    (UNIT_UNITS, 'Unidades'),
)
