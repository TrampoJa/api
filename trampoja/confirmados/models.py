from django.db import models
from ofertas.models import Ofertas


class Confirmados(models.Model):

    oferta = models.ForeignKey(
        Ofertas,
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )

    owner = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='confirmados',
        null=True,
        blank=True
    )

    create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.oferta.nome.capitalize() + self.owner.first_name.capitalize()

    class Meta:
        verbose_name = 'confirmado'
        verbose_name_plural = 'confirmados'
        ordering = ['-create']
