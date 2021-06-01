from django.db import models
from ofertas.models import Ofertas


class Avaliacoes(models.Model):

    nota = models.IntegerField(
        default=5,
        null=False,
        blank=False
    )

    owner = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='avaliacao',
        null=True,
        blank=True
    )

    oferta = models.ForeignKey(
        Ofertas,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nota

    class Meta:
        verbose_name = 'avaliacao'
        verbose_name_plural = 'avaliacoes'
        ordering = ['nota']
