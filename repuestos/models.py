
from django.db import models
from django.core.validators import MinValueValidator


class Repuesto(models.Model):
    id_repuesto = models.AutoField(primary_key=True)

    nombre_pieza = models.CharField(
        max_length=100,
        verbose_name='Nombre del repuesto'
    )

    costo = models.IntegerField(
        validators=[MinValueValidator(0)],
        verbose_name='Costo'
    )

    cantidad = models.PositiveIntegerField(
        default=0,
        verbose_name='Cantidad disponible'
    )

    class Meta:
        db_table = 'repuestos'
        ordering = ['nombre_pieza']
        verbose_name = 'Repuesto'
        verbose_name_plural = 'Repuestos'

    def __str__(self):
        return self.nombre_pieza

    @property
    def costo_formateado(self):
        return f'{self.costo:,}'.replace(',', '.')
