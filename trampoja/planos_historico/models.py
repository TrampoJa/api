from django.db import models
from estabelecimentos.models import Estabelecimentos
from planos.models import Planos


class Historico(models.Model):

    estabelecimento = models.ForeignKey(
        Estabelecimentos,
        on_delete=models.CASCADE,
        null = False,
        blank = False
    )

    plano = models.ForeignKey(
        Planos,
        on_delete=models.CASCADE,
        null = False,
        blank = False
    )

    create = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'historico'
        verbose_name_plural = 'historicos'
        ordering = ['create']