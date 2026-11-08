from django.db import models
from clientes.models import Cliente
from reparaciones.models import Reparacion


class Turno(models.Model):

    ESTADOS = [
        ('Pendiente', 'Pendiente'),
        ('Confirmado', 'Confirmado'),
        ('Cancelado', 'Cancelado'),
        ('Realizado', 'Realizado'),
    ]

    id_turno = models.AutoField(primary_key=True)

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_cliente',
        related_name='turnos'
    )

    reparacion = models.ForeignKey(
        Reparacion,
        on_delete=models.PROTECT,
        db_column='id_reparacion',
        related_name='turnos'
    )

    hora = models.TimeField()

    fecha = models.DateField()

    comentarios = models.TextField(
        null=True,
        blank=True
    )

    estado = models.CharField(
        max_length=30,
        choices=ESTADOS,
        default='Pendiente'
    )

    class Meta:
        db_table = 'turnos'
        ordering = ['fecha', 'hora']
        verbose_name = 'Turno'
        verbose_name_plural = 'Turnos'

        constraints = [
            models.UniqueConstraint(
                fields=['fecha', 'hora'],
                name='turno_fecha_hora_unicos'
            )
        ]

    def __str__(self):
        return f'Turno {self.id_turno} - {self.fecha} {self.hora}'