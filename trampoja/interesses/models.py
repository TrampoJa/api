from django.db import models
from ofertas.models import Ofertas


class Interesses(models.Model):

    oferta = models.ForeignKey(
        Ofertas,
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )

    owner = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='interesses',
        null=True,
        blank=True
    )

    create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.oferta.nome

    class Meta:
        verbose_name = 'interesse'
        verbose_name_plural = 'interesses'
        ordering = ['-create']
