from django.db import models
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User


def upload_path(instance, filename):
    return ''.join(['logos/', str(instance.owner)+'/', filename])
 

class Estabelecimentos(models.Model):
    
    owner = models.OneToOneField(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='estabelecimento',
        null  = True,
        blank = True
    )
    
    nome = models.CharField(
        max_length = 255,
        null = False,
        blank = False
    )

    cpf_cnpj = models.CharField(
        max_length = 14,
        unique = True,
        null = True,
        blank = True
    )

    razao_social = models.CharField(
        max_length = 255,
        null = True,
        blank = True
    )
    
    tipo = models.CharField(
        max_length = 255,
        null = False,
        blank = False
	)
    
    telefone = models.CharField(
		max_length = 16,
		null = False,
		blank = False
	)

    logo = models.ImageField(
        null = True,
		blank = True,
        upload_to = upload_path
    )

    create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome.lower().capitalize()

    class Meta:
        verbose_name = 'estabelecimento'
        verbose_name_plural = 'estabelecimentos'
        ordering = ['nome']