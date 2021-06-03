from django.db import models


class Enderecos(models.Model):

    pais = models.CharField(
        max_length=255,
        default="Brasil",
        null=True,
        blank=True
    )

    estado = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    cidade = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    bairro = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    rua = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    numero = models.CharField(
        max_length=10,
        null=True,
        blank=True
    )

    complemento = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    logradouro = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    owner = models.OneToOneField(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='endereco',
        null=True,
        blank=True
    )

    latitude = models.CharField(max_length=30)
    longitude = models.CharField(max_length=30)

    create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.rua.capitalize()

    class Meta:
        verbose_name = 'endereco'
        verbose_name_plural = 'enderecos'
        ordering = ['create']
