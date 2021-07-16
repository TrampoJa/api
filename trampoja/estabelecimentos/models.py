from django.db import models
from planos.models import Planos
from .managers import EstabelecimentoManager
from django.conf import settings


def upload_path(instance, filename):
    return ''.join(['estabelecimento/logos/', str(instance.owner) + '/', filename])


class Estabelecimentos(models.Model):

    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='estabelecimento',
        null=True,
        blank=True
    )

    nome = models.CharField(
        max_length=255,
        null=False,
        blank=False
    )

    cnpj = models.CharField(
        max_length=14,
        unique=True,
        null=True,
        blank=True
    )

    razao_social = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    tipo = models.CharField(
        max_length=255,
        null=False,
        blank=False
    )

    telefone = models.CharField(
        max_length=16,
        null=False,
        blank=False
    )

    logo = models.ImageField(
        null=True,
        blank=True,
        upload_to=upload_path
    )

    plano_contratado = models.ForeignKey(
        Planos,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    ofertas_para_publicar = models.IntegerField(
        default=0,
        null=True,
        blank=True
    )

    manager = EstabelecimentoManager()

    create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome.capitalize()

    class Meta:
        verbose_name = 'estabelecimento'
        verbose_name_plural = 'estabelecimentos'
        ordering = ['nome']
