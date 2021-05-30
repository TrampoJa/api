from django.db import models
from rest_framework.exceptions import ValidationError, NotFound, PermissionDenied

from .utils import *

from users.serializers import UserSerializer


class EstabelecimentoManager(models.Manager):
    def get_estabelecimento(self, pk):
        try:
            return self.get(pk=pk)
        except Exception:
            raise NotFound(detail=["Estabelecimento não encontrado."])

    def get_profile(self, user):
        try:
            return self.get(owner=user)
        except Exception:
            raise NotFound(detail=["Estabelecimento não encontrado."])

    def create_estabelecimento(self, estabelecimento, user):
        Utils.validator(estabelecimento.validated_data)
        estabelecimento.save(owner=user)
        user = self.set_group(user)
        return [estabelecimento.data, user.data]

    def set_group(self, user):
        user.last_name = "Estabelecimento"
        user.save()
        user = UserSerializer(user)
        return user

    def update(self, estabelecimento):
        Utils.validator(estabelecimento.validated_data)
        estabelecimento.save()
        return estabelecimento.data

    def set_logo(self, estabelecimento, logo):
        estabelecimento.logo = logo
        estabelecimento.save()