from django.db import models
from freelancers.models import FreeLancers

from ofertas.models import Ofertas

from .manager import ReporteManager, MotivoManager


class Motivos(models.Model):

    motivo = models.IntegerField(null=False)

    nome = models.CharField(
        max_length=255,
        null=False,
        blank=False,
    )

    manager = MotivoManager()

    created = models.DateTimeField(auto_now_add=True)


class Reportes(models.Model):
    
    freelancer = models.ForeignKey(
        FreeLancers,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )

    descricao = models.TextField(
        null=True,
        blank=True
    )

    trampo = models.ForeignKey(
        Ofertas,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )

    motivos = models.ManyToManyField(Motivos)

    manager = ReporteManager()

    created = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name = 'reporte'
        verbose_name_plural = 'reportes'
        ordering = ['-created']


