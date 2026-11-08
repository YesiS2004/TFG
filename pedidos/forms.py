from django import forms
from .models import Pedido
from proveedores.models import Proveedor


class PedidoForm(forms.ModelForm):

    proveedor = forms.ModelChoiceField(
        queryset=Proveedor.objects.all().order_by('nombre'),
        label='Proveedor',
        empty_label='Seleccione un proveedor',
        widget=forms.Select(attrs={
            'class': 'campo-formulario'
        })
    )

    repuestos_data = forms.CharField(
        required=False,
        widget=forms.HiddenInput()
    )

    class Meta:
        model = Pedido
        fields = [
            'proveedor',
            'fecha_pedido',
            'estado'
        ]

        labels = {
            'proveedor': 'Proveedor',
            'fecha_pedido': 'Fecha del pedido',
            'estado': 'Estado',
        }

        widgets = {
            'fecha_pedido': forms.DateInput(attrs={
                'class': 'campo-formulario',
                'type': 'date'
            }),
            'estado': forms.Select(attrs={
                'class': 'campo-formulario'
            }),
        }