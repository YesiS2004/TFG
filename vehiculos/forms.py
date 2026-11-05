from django import forms
from .models import Vehiculo


class VehiculoForm(forms.ModelForm):

    class Meta:
        model = Vehiculo
        fields = [
            'cliente',
            'modelo',
            'anio',
            'matricula',
            'chasis',
            'color',
        ]

        labels = {
            'cliente': 'Cliente',
            'modelo': 'Modelo',
            'anio': 'Año',
            'matricula': 'Matrícula',
            'chasis': 'Número de chasis',
            'color': 'Color',
        }

        widgets = {
            'cliente': forms.Select(attrs={
                'class': 'campo-formulario'
            }),
            'modelo': forms.Select(attrs={
                'class': 'campo-formulario'
            }),
            'anio': forms.NumberInput(attrs={
                'class': 'campo-formulario',
                'placeholder': 'Ej. 2020',
                'min': 1900,
                'max': 2100
            }),
            'matricula': forms.TextInput(attrs={
                'class': 'campo-formulario',
                'placeholder': 'Ingrese la matrícula',
                'style': 'text-transform: uppercase;'
            }),
            'chasis': forms.TextInput(attrs={
                'class': 'campo-formulario',
                'placeholder': 'Ingrese el número de chasis',
                'style': 'text-transform: uppercase;'
            }),
            'color': forms.Select(attrs={
                'class': 'campo-formulario'
            }),
        }

    def clean_matricula(self):
        matricula = self.cleaned_data['matricula']
        return matricula.upper()

    def clean_chasis(self):
        chasis = self.cleaned_data['chasis']
        return chasis.upper()