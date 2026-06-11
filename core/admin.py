"""
Configuraciones personalizadas para Django Admin
"""

from django.contrib import admin


class BaseAdmin(admin.ModelAdmin):
    """
    Clase base para administradores personalizados
    """
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
    list_per_page = 25
    
    def get_list_display(self, request):
        """Obtiene campos a mostrar en lista"""
        list_display = list(super().get_list_display(request))
        if 'created_at' in list_display and 'updated_at' in list_display:
            # Mostrar solo created_at para no saturar
            if 'updated_at' in list_display:
                list_display.remove('updated_at')
        return list_display


class TimestampedModelAdmin(BaseAdmin):
    """
    Admin para modelos con timestamps
    """
    fields = []
    
    def get_readonly_fields(self, request, obj=None):
        """Hace timestamps readonly"""
        readonly = list(super().get_readonly_fields(request, obj))
        if obj:
            readonly.extend(['created_at', 'updated_at'])
        return readonly


class ExportableAdmin(BaseAdmin):
    """
    Admin que permite exportar datos
    """
    actions = ['export_as_csv']
    
    def export_as_csv(self, request, queryset):
        """Acción para exportar como CSV"""
        import csv
        from django.http import HttpResponse
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="export.csv"'
        
        writer = csv.writer(response)
        # Escribir headers
        if queryset:
            model = queryset.model
            fields = [field.name for field in model._meta.fields]
            writer.writerow(fields)
            
            # Escribir datos
            for obj in queryset:
                writer.writerow([getattr(obj, field) for field in fields])
        
        return response
    
    export_as_csv.short_description = 'Exportar seleccionados como CSV'
