from django import forms
from .models import ProductionProcess

class ProductionProcessForm(forms.ModelForm):
    class Meta:
        model = ProductionProcess
        fields = ['product', 'quantity', 'status']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
