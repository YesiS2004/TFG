from django.db import models
from vehiculos.models import Vehiculo
from repuestos.models import Repuesto
from servicios.models import Servicio


class Reparacion(models.Model):

    ESTADOS = [
        ('Pendiente', 'Pendiente'),
        ('En proceso', 'En proceso'),
        ('Terminada', 'Terminada'),
        ('Entregada', 'Entregada'),
    ]

    id_reparacion = models.AutoField(primary_key=True)

    vehiculo = models.ForeignKey(
        Vehiculo,
        on_delete=models.PROTECT,
        db_column='id_vehiculo',
        related_name='reparaciones'
    )

    descripcion = models.TextField(
        null=True,
        blank=True
    )

    estado = models.CharField(
        max_length=30,
        choices=ESTADOS,
        default='Pendiente'
    )

    class Meta:
        db_table = 'reparaciones'
        ordering = ['-id_reparacion']
        verbose_name = 'Reparación'
        verbose_name_plural = 'Reparaciones'

    def __str__(self):
        return f'Reparación {self.id_reparacion}'


class ReparacionRepuesto(models.Model):

    id_reparacion_repuesto = models.AutoField(primary_key=True)

    reparacion = models.ForeignKey(
        Reparacion,
        on_delete=models.CASCADE,
        db_column='id_reparacion',
        related_name='repuestos_utilizados'
    )

    repuesto = models.ForeignKey(
        Repuesto,
        on_delete=models.PROTECT,
        db_column='id_repuesto',
        related_name='reparaciones'
    )

    cantidad = models.PositiveIntegerField(default=1)

    class Meta:
        db_table = 'reparacion_repuesto'
        verbose_name = 'Repuesto utilizado'
        verbose_name_plural = 'Repuestos utilizados'
        constraints = [
            models.UniqueConstraint(
                fields=['reparacion', 'repuesto'],
                name='repuesto_unico_por_reparacion'
            )
        ]

    def __str__(self):
        return f'{self.repuesto} - {self.cantidad}'


class ReparacionServicio(models.Model):

    id_reparacion_servicio = models.AutoField(primary_key=True)

    reparacion = models.ForeignKey(
        Reparacion,
        on_delete=models.CASCADE,
        db_column='id_reparacion',
        related_name='servicios_realizados'
    )

    servicio = models.ForeignKey(
        Servicio,
        on_delete=models.PROTECT,
        db_column='id_servicio',
        related_name='reparaciones'
    )

    class Meta:
        db_table = 'reparacion_servicio'
        verbose_name = 'Servicio de reparación'
        verbose_name_plural = 'Servicios de reparación'
        constraints = [
            models.UniqueConstraint(
                fields=['reparacion', 'servicio'],
                name='servicio_unico_por_reparacion'
            )
        ]

    def __str__(self):
        return f'{self.reparacion} - {self.servicio}'