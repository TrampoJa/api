from django.db import models
from django.conf import settings


def upload_path(instance, filename):
    return ''.join(['freelancers/fotos/', str(instance.owner) + '/', filename])

def upload_path_docs(instance, filename):
    return ''.join(['freelancers/docs/',
        str(f'{instance.freelancer_id}-{instance.freelancer}') + '/', filename])


class FreeLancers(models.Model):

    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='freelancer',
        null=True,
        blank=True
    )

    nome = models.CharField(
        max_length=255,
        null=False,
        blank=False
    )

    sobrenome = models.CharField(
        max_length=255,
        null=False,
        blank=False
    )

    telefone = models.CharField(
        max_length=16,
        null=False,
        blank=False
    )

    nascimento = models.DateField(
        null=True,
        blank=True
    )

    foto = models.ImageField(
        null=True,
        blank=True,
        upload_to=upload_path
    )

    rg = models.CharField(
        max_length=16,
        unique=True,
        null=True,
        blank=True
    )

    bio = models.TextField()

    verificado = models.BooleanField(
        default=False,
        null=True,
        blank=True
    )

    create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome.capitalize() + ' ' + self.sobrenome.capitalize()

    class Meta:
        verbose_name = 'freelancer'
        verbose_name_plural = 'freelancers'
        ordering = ['create']


class Documentos(models.Model):

    freelancer = models.OneToOneField(
        FreeLancers,
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )

    frente = models.ImageField(
        null=True,
        blank=True,
        upload_to=upload_path_docs
    )

    verso = models.ImageField(
        null=True,
        blank=True,
        upload_to=upload_path_docs
    )

    selfie = models.ImageField(
        null=True,
        blank=True,
        upload_to=upload_path_docs
    )

    create = models.DateTimeField(auto_now_add=True)


