
from django import forms
from .models import Marca, Modelo


class MarcaForm(forms.ModelForm):
    class Meta:
        model = Marca
        fields = ['nombre_marca']
        labels = {
            'nombre_marca': 'Nombre de la marca',
        }
        widgets = {
            'nombre_marca': forms.TextInput(attrs={
                'placeholder': 'Ej.: Toyota',
                'maxlength': 50,
            }),
        }

    def clean_nombre_marca(self):
        nombre = self.cleaned_data['nombre_marca'].strip()

        if not nombre:
            raise forms.ValidationError(
                'El nombre de la marca es obligatorio.'
            )

        duplicado = Marca.objects.filter(
            nombre_marca__iexact=nombre
        )

        if self.instance.pk:
            duplicado = duplicado.exclude(pk=self.instance.pk)

        if duplicado.exists():
            raise forms.ValidationError(
                'Esta marca ya se encuentra registrada.'
            )

        return nombre


class ModeloForm(forms.ModelForm):
    class Meta:
        model = Modelo
        fields = ['marca', 'nombre_modelo']
        labels = {
            'marca': 'Marca',
            'nombre_modelo': 'Nombre del modelo',
        }
        widgets = {
            'marca': forms.Select(),
            'nombre_modelo': forms.TextInput(attrs={
                'placeholder': 'Ej.: Corolla',
                'maxlength': 100,
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['marca'].empty_label = 'Seleccione una marca'
        self.fields['marca'].queryset = Marca.objects.order_by(
            'nombre_marca'
        )

    def clean_nombre_modelo(self):
        nombre = self.cleaned_data['nombre_modelo'].strip()
        marca = self.cleaned_data.get('marca')

        if not nombre:
            raise forms.ValidationError(
                'El nombre del modelo es obligatorio.'
            )

        duplicado = Modelo.objects.filter(
            marca=marca,
            nombre_modelo__iexact=nombre
        )

        if self.instance.pk:
            duplicado = duplicado.exclude(pk=self.instance.pk)

        if duplicado.exists():
            raise forms.ValidationError(
                'Este modelo ya está registrado para la marca seleccionada.'
            )

        return nombre
