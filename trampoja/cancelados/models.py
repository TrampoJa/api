from django.db import models
from ofertas.models import Ofertas


class Cancelados(models.Model):

    oferta = models.OneToOneField(
        Ofertas,
        on_delete=models.CASCADE,
        null=False,
    )

    owner = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    justificativa = models.TextField(
        null=False,
        blank=False
    )

    autor = models.CharField(
        max_length=1,
        null=False,
        blank=True
    )

    create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.justificativa

    class Meta:
        verbose_name = 'cancelado'
        verbose_name_plural = 'cancelados'
        ordering = ['oferta']
