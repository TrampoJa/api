from django.db import models
from django.contrib.auth.models import User


class User(User):
    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'usuario'
        verbose_name_plural = 'usuarios'
        ordering = ['username']
