
import re

from django import forms
from .models import Cliente


class ClienteForm(forms.ModelForm):

    class Meta:
        model = Cliente
        fields = [
            'nombre',
            'apellido',
            'documento',
            'telefono',
            'email',
        ]

        labels = {
            'nombre': 'Nombre',
            'apellido': 'Apellido',
            'documento': 'Número de documento',
            'telefono': 'Número de teléfono',
            'email': 'Correo electrónico',
        }

        widgets = {
            'nombre': forms.TextInput(attrs={
                'placeholder': 'Ingrese el nombre',
                'maxlength': 100,
            }),
            'apellido': forms.TextInput(attrs={
                'placeholder': 'Ingrese el apellido',
                'maxlength': 100,
            }),
            'documento': forms.TextInput(attrs={
                'placeholder': 'Ingrese el número de documento',
                'maxlength': 20,
            }),
            'telefono': forms.TextInput(attrs={
                'placeholder': 'Ingrese el número de teléfono',
                'maxlength': 20,
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Ingrese el correo electrónico (opcional)',
                'maxlength': 254,
            }),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre'].strip()

        if not nombre:
            raise forms.ValidationError(
                'El nombre es obligatorio.'
            )

        if not all(
            caracter.isalpha() or caracter in " -'"
            for caracter in nombre
        ):
            raise forms.ValidationError(
                'El nombre solo puede contener letras, espacios, '
                'guiones y apóstrofes.'
            )

        return nombre

    def clean_apellido(self):
        apellido = self.cleaned_data['apellido'].strip()

        if not apellido:
            raise forms.ValidationError(
                'El apellido es obligatorio.'
            )

        if not all(
            caracter.isalpha() or caracter in " -'"
            for caracter in apellido
        ):
            raise forms.ValidationError(
                'El apellido solo puede contener letras, espacios, '
                'guiones y apóstrofes.'
            )

        return apellido

    def clean_documento(self):
        documento = self.cleaned_data['documento'].strip()

        if not documento:
            raise forms.ValidationError(
                'El número de documento es obligatorio.'
            )

        if not re.fullmatch(r'[0-9.\-\s]+', documento):
            raise forms.ValidationError(
                'El documento solo puede contener números, puntos '
                'y guiones.'
            )

        duplicado = Cliente.objects.filter(
            documento__iexact=documento
        )

        if self.instance.pk:
            duplicado = duplicado.exclude(pk=self.instance.pk)

        if duplicado.exists():
            raise forms.ValidationError(
                'Ya existe un cliente con ese número de documento.'
            )

        return documento

    def clean_telefono(self):
        telefono = self.cleaned_data['telefono'].strip()

        if not telefono:
            raise forms.ValidationError(
                'El número de teléfono es obligatorio.'
            )

        if not re.fullmatch(r'[0-9+\-\s()]+', telefono):
            raise forms.ValidationError(
                'El teléfono contiene caracteres no válidos.'
            )

        cantidad_digitos = sum(
            caracter.isdigit() for caracter in telefono
        )

        if cantidad_digitos < 6:
            raise forms.ValidationError(
                'El teléfono debe contener al menos 6 dígitos.'
            )

        return telefono

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip()
        return email
