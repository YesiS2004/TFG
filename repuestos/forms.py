
from django import forms
from .models import Repuesto


class RepuestoForm(forms.ModelForm):

    class Meta:
        model = Repuesto
        fields = [
            'nombre_pieza',
            'costo',
            'cantidad',
        ]

        widgets = {
            'nombre_pieza': forms.TextInput(attrs={
                'placeholder': 'Ingrese el nombre del repuesto'
            }),

            'costo': forms.NumberInput(attrs={
                'placeholder': 'Ingrese el costo',
                'min': '0'
            }),

            'cantidad': forms.NumberInput(attrs={
                'placeholder': 'Ingrese la cantidad disponible',
                'min': '0'
            }),
        }

        labels = {
            'nombre_pieza': 'Nombre del repuesto',
            'costo': 'Costo (Gs.)',
            'cantidad': 'Cantidad disponible',
        }
