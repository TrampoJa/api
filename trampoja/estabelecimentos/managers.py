from django.db import models
from rest_framework.exceptions import ValidationError, NotFound, PermissionDenied

from utils.validator import Validator

from users.serializers import UserSerializer
from users.models import User


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
        Validator(estabelecimento.validated_data)
        estabelecimento.save(owner=user)
        user = self.set_group(user)
        return [estabelecimento.data, user.data]

    def set_group(self, user):
        user = User.set_group(user, "Estabelecimento")
        user = UserSerializer(user)
        return user

    def update(self, estabelecimento):
        Validator(estabelecimento.validated_data)
        estabelecimento.save()
        return estabelecimento.data

    def set_logo(self, estabelecimento, logo):
        estabelecimento.logo = logo
        estabelecimento.save()
