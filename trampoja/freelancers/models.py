from django.db import models


def upload_path(instance, filename):
    return ''.join(['fotos/', str(instance.owner) + '/', filename])


class FreeLancers(models.Model):

    owner = models.OneToOneField(
        'auth.User',
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
        null=False,
        blank=False,
        upload_to=upload_path
    )

    verso = models.ImageField(
        null=False,
        blank=False,
        upload_to=upload_path
    )

    selfie = models.ImageField(
        null=False,
        blank=False,
        upload_to=upload_path
    )

    create = models.DateTimeField(auto_now_add=True)


