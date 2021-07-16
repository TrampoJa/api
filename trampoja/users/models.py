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

    
'''
FAZER BACKUP BD -> MODELO ANTIGO

REALIZAR EXPORT DE TODAS AS TABELAS -> MODELO NOVO

DROPAR BANCO

CRIAR BANCO NOVAMENTE

BAIXAR ESSA BRANCH

RODAR MIGRATIONS

REALIZAR OS IMPORTS DE TODAS AS TABELAS

ALTERAR SEQUENCIA DE IDS:
-- SELECT MAX(id) FROM users_user;
-- Select nextval(pg_get_serial_sequence('users_user', 'id'));

-- SELECT setval(pg_get_serial_sequence('users_user', 'id'), (SELECT MAX(id) FROM users_user)+1);

MESCLAR COM A DEV, SUBIR BETA E MASTER
'''