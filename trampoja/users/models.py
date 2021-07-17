from django.contrib.auth.models import Group, AbstractUser
from django.db import models

class User(AbstractUser):

    telefone = models.CharField(
        max_length=16,
        null=True,
        blank=True
    )
    
    def set_group(self, groupName):
        try:
            group = Group.objects.get_by_natural_key(groupName)
            self.groups.set([group])
        except Group.DoesNotExist:
            ...