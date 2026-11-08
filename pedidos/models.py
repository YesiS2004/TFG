from django.db import models
from proveedores.models import Proveedor
from repuestos.models import Repuesto


class Pedido(models.Model):

    ESTADOS = [
        ('Pendiente', 'Pendiente'),
        ('Enviado', 'Enviado'),
        ('Recibido', 'Recibido'),
        ('Cancelado', 'Cancelado'),
    ]

    id_pedido = models.AutoField(primary_key=True)

    proveedor = models.ForeignKey(
        Proveedor,
        on_delete=models.PROTECT,
        db_column='id_proveedor',
        related_name='pedidos'
    )

    fecha_pedido = models.DateField()

    estado = models.CharField(
        max_length=30,
        choices=ESTADOS,
        default='Pendiente'
    )

    class Meta:
        db_table = 'pedidos'
        ordering = ['-fecha_pedido', '-id_pedido']
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'

    def __str__(self):
        return f'Pedido {self.id_pedido}'


class DetallePedido(models.Model):

    id_detalle_pedido = models.AutoField(primary_key=True)

    repuesto = models.ForeignKey(
        Repuesto,
        on_delete=models.PROTECT,
        db_column='id_repuesto',
        related_name='detalles_pedido'
    )

    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        db_column='id_pedido',
        related_name='detalles'
    )

    cantidad = models.PositiveIntegerField(default=1)

    class Meta:
        db_table = 'detalle_pedido'
        verbose_name = 'Detalle del pedido'
        verbose_name_plural = 'Detalles del pedido'

        constraints = [
            models.UniqueConstraint(
                fields=['pedido', 'repuesto'],
                name='repuesto_unico_por_pedido'
            )
        ]

    def __str__(self):
        return f'{self.repuesto} - {self.cantidad}'