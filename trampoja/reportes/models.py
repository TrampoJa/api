from django.db import models
from freelancers.models import FreeLancers


class Motivos(models.Model):

    motivo = models.IntegerField(null=False)

    nome = models.CharField(
        max_length=255,
        null=False,
        blank=False,
    )

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

    motivos = models.ManyToManyField(Motivos)

    created = models.DateTimeField(auto_now_add=True)


