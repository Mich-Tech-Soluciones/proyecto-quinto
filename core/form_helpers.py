"""
Helpers para manejo de formularios
"""

from django import forms
from django.forms.widgets import DateInput, TimeInput, DateTimeInput


class BootstrapForm(forms.ModelForm):
    """
    Formulario base que añade clases Bootstrap a los campos
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_bootstrap_classes()
    
    def add_bootstrap_classes(self):
        """Añade clases Bootstrap a todos los campos"""
        for field_name, field in self.fields.items():
            # Añadir clase base
            css_classes = 'form-control'
            
            # Clases específicas por tipo
            if isinstance(field.widget, forms.CheckboxInput):
                css_classes = 'form-check-input'
            elif isinstance(field.widget, (forms.Select, forms.RadioSelect)):
                css_classes = 'form-select'
            elif isinstance(field.widget, forms.Textarea):
                css_classes = 'form-control'
            elif isinstance(field.widget, (DateInput, TimeInput, DateTimeInput)):
                css_classes = 'form-control'
            
            # Aplicar clases
            current_classes = field.widget.attrs.get('class', '')
            if current_classes:
                css_classes = f'{current_classes} {css_classes}'
            
            field.widget.attrs['class'] = css_classes
            
            # Añadir placeholder si es texto
            if isinstance(field.widget, (forms.TextInput, forms.EmailInput)):
                field.widget.attrs['placeholder'] = field.label or field_name


class SearchForm(forms.Form):
    """
    Formulario de búsqueda simple
    """
    query = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar...',
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_bootstrap_classes()
    
    def add_bootstrap_classes(self):
        """Añade clases Bootstrap"""
        for field in self.fields.values():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'


class FilterForm(forms.Form):
    """
    Formulario base para filtros
    """
    start_date = forms.DateField(
        required=False,
        widget=DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
        })
    )
    end_date = forms.DateField(
        required=False,
        widget=DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_bootstrap_classes()
    
    def add_bootstrap_classes(self):
        """Añade clases Bootstrap"""
        for field in self.fields.values():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'
