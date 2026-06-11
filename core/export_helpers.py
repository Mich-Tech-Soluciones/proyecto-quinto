"""
Helpers para importar y exportar datos
"""

import csv
import json
from django.http import HttpResponse
from decimal import Decimal


def export_to_csv(queryset, fields, filename='export.csv'):
    """
    Exporta un QuerySet a CSV
    
    Args:
        queryset: QuerySet a exportar
        fields: Campos a incluir
        filename: Nombre del archivo
    
    Returns:
        HttpResponse: Respuesta con archivo CSV
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    writer = csv.writer(response)
    
    # Escribir headers
    writer.writerow(fields)
    
    # Escribir datos
    for obj in queryset:
        row = []
        for field in fields:
            value = getattr(obj, field, '')
            # Convertir Decimal a string
            if isinstance(value, Decimal):
                value = str(value)
            row.append(value)
        writer.writerow(row)
    
    return response


def export_to_json(data, filename='export.json'):
    """
    Exporta datos a JSON
    
    Args:
        data: Datos a exportar
        filename: Nombre del archivo
    
    Returns:
        HttpResponse: Respuesta con archivo JSON
    """
    response = HttpResponse(content_type='application/json')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    response.write(json.dumps(data, indent=2, default=str))
    
    return response


def import_from_csv(file_path):
    """
    Importa datos desde un archivo CSV
    
    Args:
        file_path: Ruta del archivo
    
    Returns:
        list: Lista de diccionarios
    """
    data = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data.append(row)
    except Exception as e:
        print(f"Error importando CSV: {e}")
    
    return data


def import_from_json(file_path):
    """
    Importa datos desde un archivo JSON
    
    Args:
        file_path: Ruta del archivo
    
    Returns:
        dict o list: Datos importados
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as jsonfile:
            return json.load(jsonfile)
    except Exception as e:
        print(f"Error importando JSON: {e}")
        return {}


class DataExporter:
    """Clase para exportar datos"""
    
    def __init__(self, queryset, fields):
        self.queryset = queryset
        self.fields = fields
    
    def to_csv(self, filename='export.csv'):
        """Exporta a CSV"""
        return export_to_csv(self.queryset, self.fields, filename)
    
    def to_json(self, filename='export.json'):
        """Exporta a JSON"""
        data = []
        for obj in self.queryset:
            row = {}
            for field in self.fields:
                value = getattr(obj, field, '')
                if isinstance(value, Decimal):
                    value = float(value)
                row[field] = value
            data.append(row)
        
        return export_to_json(data, filename)
