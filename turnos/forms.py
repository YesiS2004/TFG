from django import forms
from .models import Turno
from reparaciones.models import Reparacion


class ReparacionChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        vehiculo = obj.vehiculo
        return (
            f'{vehiculo.cliente} - '
            f'{vehiculo.matricula} - '
            f'{vehiculo.modelo} - '
            f'Reparación {obj.id_reparacion}'
        )


class TurnoForm(forms.ModelForm):

    reparacion = ReparacionChoiceField(
        queryset=Reparacion.objects.select_related(
            'vehiculo__cliente',
            'vehiculo__modelo__marca'
        ).all(),
        label='Reparación',
        widget=forms.Select(attrs={
            'class': 'campo-formulario'
        })
    )

    class Meta:
        model = Turno
        fields = [
            'cliente',
            'reparacion',
            'fecha',
            'hora',
            'comentarios',
            'estado'
        ]

        labels = {
            'cliente': 'Cliente',
            'reparacion': 'Reparación',
            'fecha': 'Fecha del turno',
            'hora': 'Hora del turno',
            'comentarios': 'Comentarios',
            'estado': 'Estado',
        }

        widgets = {
            'cliente': forms.Select(attrs={
                'class': 'campo-formulario'
            }),
            'fecha': forms.DateInput(attrs={
                'class': 'campo-formulario',
                'type': 'date'
            }),
            'hora': forms.TimeInput(attrs={
                'class': 'campo-formulario',
                'type': 'time'
            }),
            'comentarios': forms.Textarea(attrs={
                'class': 'campo-formulario',
                'placeholder': 'Ingrese algún comentario (opcional)',
                'rows': 3
            }),
            'estado': forms.Select(attrs={
                'class': 'campo-formulario'
            }),
        }