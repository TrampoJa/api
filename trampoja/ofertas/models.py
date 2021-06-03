from django.db import models


class Ofertas(models.Model):

    nome = models.CharField(
        max_length=255,
        null=False,
        blank=False
    )

    valor = models.IntegerField(
        null=False,
        blank=False
    )

    time = models.TimeField(
        null=True,
        blank=True
    )

    time_final = models.TimeField(
        null=True,
        blank=True
    )

    date_inicial = models.DateField(
        null=True,
        blank=True
    )

    obs = models.TextField(
        null=True,
        blank=True
    )

    owner = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='ofertas',
        null=True,
        blank=True
    )

    create = models.DateTimeField(auto_now_add=True)

    status = models.BooleanField(
        default=True,
        null=True,
        blank=True
    )

    edit = models.BooleanField(
        default=True,
        null=True,
        blank=True
    )

    canceled = models.BooleanField(
        default=False,
        null=True,
        blank=True
    )

    closed = models.BooleanField(
        default=False,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.nome.capitalize()

    class Meta:
        verbose_name = 'oferta'
        verbose_name_plural = 'ofertas'
        ordering = ['-status', 'date_inicial', 'time']
