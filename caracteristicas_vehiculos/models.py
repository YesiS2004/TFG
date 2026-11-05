
from django.db import models


class Marca(models.Model):
    id_marca = models.AutoField(primary_key=True)
    nombre_marca = models.CharField(max_length=50)

    class Meta:
        db_table = 'marcas'
        ordering = ['nombre_marca']
        verbose_name = 'Marca'
        verbose_name_plural = 'Marcas'

    def __str__(self):
        return self.nombre_marca


class Modelo(models.Model):
    id_modelo = models.AutoField(primary_key=True)
    marca = models.ForeignKey(
        Marca,
        on_delete=models.PROTECT,
        db_column='id_marca',
        related_name='modelos'
    )
    nombre_modelo = models.CharField(max_length=100)

    class Meta:
        db_table = 'modelos'
        ordering = ['nombre_modelo']
        verbose_name = 'Modelo'
        verbose_name_plural = 'Modelos'
        constraints = [
            models.UniqueConstraint(
                fields=['marca', 'nombre_modelo'],
                name='modelo_unico_por_marca'
            )
        ]

    def __str__(self):
        return f'{self.marca.nombre_marca} - {self.nombre_modelo}'


class Color(models.Model):
    id_color = models.AutoField(primary_key=True)
    color = models.CharField(max_length=40, unique=True)

    class Meta:
        db_table = 'colores'
        ordering = ['color']
        verbose_name = 'Color'
        verbose_name_plural = 'Colores'

    def __str__(self):
        return self.color
