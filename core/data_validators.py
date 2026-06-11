"""
Helpers para validación de datos
"""

from decimal import Decimal, InvalidOperation


def is_valid_decimal(value, max_digits=10, decimal_places=2):
    """
    Valida si un valor es un decimal válido
    
    Args:
        value: Valor a validar
        max_digits: Máximo número de dígitos
        decimal_places: Máximo número de decimales
    
    Returns:
        dict: Resultado de validación
    """
    try:
        decimal_value = Decimal(str(value))
        
        # Verificar lugares decimales
        if decimal_value.as_tuple().exponent < -decimal_places:
            return {
                'valid': False,
                'error': f'Máximo {decimal_places} decimales permitidos'
            }
        
        # Verificar dígitos totales
        digit_count = len(str(decimal_value).replace('.', '').replace('-', ''))
        if digit_count > max_digits:
            return {
                'valid': False,
                'error': f'Máximo {max_digits} dígitos permitidos'
            }
        
        return {'valid': True, 'value': decimal_value}
    
    except (InvalidOperation, ValueError):
        return {'valid': False, 'error': 'Valor decimal inválido'}


def validate_date_range(start_date, end_date):
    """
    Valida un rango de fechas
    
    Args:
        start_date: Fecha de inicio
        end_date: Fecha de fin
    
    Returns:
        dict: Resultado de validación
    """
    if start_date > end_date:
        return {
            'valid': False,
            'error': 'La fecha de inicio debe ser menor que la fecha de fin'
        }
    
    return {'valid': True}


def validate_required_fields(data, required_fields):
    """
    Valida que los campos requeridos estén presentes
    
    Args:
        data: Diccionario de datos
        required_fields: Lista de campos requeridos
    
    Returns:
        dict: Resultado de validación
    """
    missing_fields = []
    
    for field in required_fields:
        if field not in data or not data[field]:
            missing_fields.append(field)
    
    if missing_fields:
        return {
            'valid': False,
            'error': f'Campos requeridos: {", ".join(missing_fields)}'
        }
    
    return {'valid': True}


def validate_quantity(quantity, min_value=1, max_value=999999):
    """
    Valida una cantidad
    
    Args:
        quantity: Cantidad a validar
        min_value: Valor mínimo
        max_value: Valor máximo
    
    Returns:
        dict: Resultado de validación
    """
    try:
        qty = int(quantity)
        
        if qty < min_value:
            return {'valid': False, 'error': f'Cantidad mínima: {min_value}'}
        
        if qty > max_value:
            return {'valid': False, 'error': f'Cantidad máxima: {max_value}'}
        
        return {'valid': True, 'value': qty}
    
    except ValueError:
        return {'valid': False, 'error': 'Cantidad debe ser un número entero'}


def validate_price(price):
    """
    Valida un precio
    
    Args:
        price: Precio a validar
    
    Returns:
        dict: Resultado de validación
    """
    result = is_valid_decimal(price, max_digits=10, decimal_places=2)
    
    if result['valid'] and result['value'] < 0:
        return {'valid': False, 'error': 'El precio no puede ser negativo'}
    
    return result


def validate_stock(stock):
    """
    Valida un nivel de stock
    
    Args:
        stock: Stock a validar
    
    Returns:
        dict: Resultado de validación
    """
    return validate_quantity(stock, min_value=0, max_value=999999)
