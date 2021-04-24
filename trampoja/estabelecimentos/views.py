from django.http import *
from django.views.decorators.csrf import csrf_protect

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import ValidationError, NotFound, PermissionDenied

from .serializers import EstabelecimentosSerializer
from .models import Estabelecimentos
from .utils import *
from .permissions import IsOwnerOrReadOnly

from users.views import get_user
from users.serializers import UserSerializer


def get_estabelecimento(pk):
    try:
        return Estabelecimentos.objects.get(pk=pk)
    except Estabelecimentos.DoesNotExist:
        raise NotFound(detail="Estabelecimento não encontrado.")


class CreateEstabelecimentoView():  
    @csrf_protect
    @api_view(['POST'])
    @authentication_classes([TokenAuthentication])
    def create(request, format=None):
        user = get_user(request.user.id)
        serializer = EstabelecimentosSerializer(data=request.data)
        if serializer.is_valid():
            Utils.validator(serializer.validated_data)
            serializer.save(owner=request.user)
            user.last_name = "Estabelecimento"
            user.save()
            userSerializer = UserSerializer(user)
            return Response([serializer.data, userSerializer.data], status=status.HTTP_201_CREATED)
        raise ValidationError(detail="Não foi possível finalizar seu cadastro, \
                verifique os dados informados e tente novamente")


class ListEstabelecimentoView():
    @api_view(['GET'])
    @authentication_classes([TokenAuthentication])
    def liste(request, format=None):
        estabelecimentos = Estabelecimentos.objects.all()
        if estabelecimentos is not None :
            serializer = EstabelecimentosSerializer(estabelecimentos, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        raise NotFound(detail="Não foi possível exibir os estabelecimentos.")


class ProfileEstabelecimentoView():
    @api_view(['GET'])
    @authentication_classes([TokenAuthentication])
    def profile(request, format=None):
        estabelecimento = Estabelecimentos.objects.get(owner_id=request.user.pk)
        if estabelecimento is not None :
            serializer = EstabelecimentosSerializer(estabelecimento)
            return Response(serializer.data, status=status.HTTP_200_OK)
        raise NotFound(detail="Não foi possível exibir seus dados.")


class DetailEstabelecimentoView():
    @api_view(['GET'])
    @authentication_classes([TokenAuthentication])
    def detail(request, pk, format=None):
        estabelecimento = get_estabelecimento(pk)
        if IsOwnerOrReadOnly.has_object_permission(request, estabelecimento):
            if estabelecimento is not None :
                serializer = EstabelecimentosSerializer(estabelecimento)
                return Response(serializer.data, status=status.HTTP_200_OK)
            raise NotFound(detail="Não foi possível exibir seus dados.")
        raise PermissionDenied(detail=["Você não tem permissão para isso."])


class UpdateEstabelecimentoView():
    @csrf_protect
    @api_view(['PUT', 'POST'])
    @authentication_classes([TokenAuthentication])
    def update(request, pk, format=None):
        estabelecimento = get_estabelecimento(pk)
        if IsOwnerOrReadOnly.has_object_permission(request, estabelecimento):
            serializer = EstabelecimentosSerializer(estabelecimento, data=request.data)
            if serializer.is_valid():
                Utils.validator(serializer.validated_data)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            raise ValidationError(detail="Não foi possível atualizar seus dados, \
                    verifique os dados informados e tente novamente.")
        raise PermissionDenied(detail=["Você não tem permissão para isso."])


class DeleteEstabelecimentoView():
    @api_view(['DELETE'])
    @authentication_classes([TokenAuthentication])
    def delete(request, pk, format=None):
        estabelecimento = get_estabelecimento(pk)
        if IsOwnerOrReadOnly.has_object_permission(request, estabelecimento):
            try:
                estabelecimento.delete()
                return Response(status=status.HTTP_200_OK)
            except Exception:
                raise ValidationError(detail="Algo deu errado.")
        raise PermissionDenied(detail=["Você não tem permissão para isso."])