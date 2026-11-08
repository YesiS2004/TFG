
from django import forms

from .models import Reparacion
from vehiculos.models import Vehiculo


class VehiculoChoiceField(forms.ModelChoiceField):

    def label_from_instance(self, obj):
        return (
            f'{obj.cliente} - {obj.matricula} - '
            f'{obj.modelo}'
        )


class ReparacionForm(forms.ModelForm):

    vehiculo = VehiculoChoiceField(
        queryset=Vehiculo.objects.select_related(
            'cliente',
            'modelo__marca'
        ).all(),
        label='Vehículo',
        widget=forms.Select(attrs={
            'class': 'campo-formulario'
        })
    )

    servicios_data = forms.CharField(
        required=False,
        widget=forms.HiddenInput()
    )

    repuestos_data = forms.CharField(
        required=False,
        widget=forms.HiddenInput()
    )

    class Meta:
        model = Reparacion
        fields = [
            'vehiculo',
            'descripcion',
            'estado',
        ]

        labels = {
            'vehiculo': 'Vehículo',
            'descripcion': 'Descripción / observaciones',
            'estado': 'Estado',
        }

        widgets = {
            'descripcion': forms.Textarea(attrs={
                'class': 'campo-formulario',
                'placeholder': 'Ingrese la descripción u observaciones del trabajo',
                'rows': 4
            }),

            'estado': forms.Select(attrs={
                'class': 'campo-formulario'
            }),
        }
