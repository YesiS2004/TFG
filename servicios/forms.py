
from django import forms
from .models import Servicio


class ServicioForm(forms.ModelForm):

    class Meta:
        model = Servicio
        fields = [
            'nombre',
            'descripcion',
            'duracion_horas',
            'costo',
        ]

        labels = {
            'nombre': 'Nombre del servicio',
            'descripcion': 'Descripción (opcional)',
            'duracion_horas': 'Duración aproximada (horas)',
            'costo': 'Costo del servicio (Gs.)',
        }

        widgets = {
            'nombre': forms.TextInput(attrs={
                'placeholder': 'Ingrese el nombre del servicio',
                'maxlength': 160,
            }),
            'descripcion': forms.Textarea(attrs={
                'placeholder': 'Ingrese una descripción (opcional)',
                'rows': 3,
            }),
            'duracion_horas': forms.NumberInput(attrs={
                'placeholder': 'Ej.: 1.5',
                'min': '0.01',
                'max': '999.99',
                'step': '0.01',
            }),
            'costo': forms.NumberInput(attrs={
                'placeholder': 'Ej.: 150000',
                'min': '1',
                'step': '1',
            }),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre'].strip()

        if not nombre:
            raise forms.ValidationError(
                'El nombre del servicio es obligatorio.'
            )

        duplicado = Servicio.objects.filter(
            nombre__iexact=nombre
        )

        if self.instance.pk:
            duplicado = duplicado.exclude(pk=self.instance.pk)

        if duplicado.exists():
            raise forms.ValidationError(
                'Ya existe un servicio con ese nombre.'
            )

        return nombre

    def clean_descripcion(self):
        return self.cleaned_data.get('descripcion', '').strip()

    def clean_duracion_horas(self):
        duracion = self.cleaned_data['duracion_horas']

        if duracion <= 0:
            raise forms.ValidationError(
                'La duración debe ser mayor que cero.'
            )

        if duracion > 999.99:
            raise forms.ValidationError(
                'La duración no puede superar las 999.99 horas.'
            )

        return duracion

    def clean_costo(self):
        costo = self.cleaned_data['costo']

        if costo < 1:
            raise forms.ValidationError(
                'El costo debe ser mayor que cero.'
            )

        return costo
