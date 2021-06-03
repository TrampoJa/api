from django.db import models
from .managers import PlanosManager


class Planos(models.Model):

    nome = models.CharField(
        max_length=255,
        null=False,
        blank=False
    )

    valor = models.IntegerField(
        null=False,
        blank=False
    )

    quantidade = models.IntegerField(
        null=True,
        blank=True
    )

    descricao = models.TextField(
        null=True,
        blank=True
    )

    especial = models.BooleanField(
        default=False,
        null=True,
        blank=True
    )

    create = models.DateTimeField(auto_now_add=True)

    manager = PlanosManager()

    def __str__(self):
        return self.nome.lower().capitalize()

    class Meta:
        verbose_name = 'plano'
        verbose_name_plural = 'planos'
        ordering = ['create']
