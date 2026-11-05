from django.db import models
from clientes.models import Cliente
from caracteristicas_vehiculos.models import Modelo, Color


class Vehiculo(models.Model):
    id_vehiculo = models.AutoField(primary_key=True)

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        db_column='id_cliente',
        related_name='vehiculos'
    )

    modelo = models.ForeignKey(
        Modelo,
        on_delete=models.PROTECT,
        db_column='id_modelo',
        related_name='vehiculos'
    )

    anio = models.IntegerField()

    matricula = models.CharField(max_length=20)

    chasis = models.CharField(max_length=50)

    color = models.ForeignKey(
        Color,
        on_delete=models.PROTECT,
        db_column='id_color',
        related_name='vehiculos'
    )

    class Meta:
        db_table = 'vehiculos'
        ordering = ['matricula']
        verbose_name = 'Vehículo'
        verbose_name_plural = 'Vehículos'

    def __str__(self):
        return f'{self.matricula} - {self.modelo}'