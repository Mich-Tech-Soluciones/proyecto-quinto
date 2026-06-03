from django import forms
from .models import Cost

class CostForm(forms.ModelForm):
    class Meta:
        model = Cost
        fields = ['production_process', 'description', 'amount']
        widgets = {
            'production_process': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }
