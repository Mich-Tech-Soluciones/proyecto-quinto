from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'customer_name',
            'customer_phone',
            'customer_email',
            'company',
            'payment_method',
            'payment_status',
            'status',
            'technical_specs',
            'notes',
            'design_image',
        ]
        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre o institución'}),
            'customer_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
            'customer_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'company': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Empresa'}),
            'payment_method': forms.Select(attrs={'class': 'form-select'}),
            'payment_status': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'technical_specs': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Especificaciones técnicas'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Notas adicionales'}),
            'design_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
