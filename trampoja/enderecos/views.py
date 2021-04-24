from django.http import *
from django.views.decorators.csrf import csrf_protect

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import ValidationError, NotFound

from .serializers import EnderecosSerializer
from .models import Enderecos


def get_endereco(pk):
    try:
        return Enderecos.objects.get(pk=pk)
    except Enderecos.DoesNotExist:
        raise NotFound(detail="Endereço não encontrado.")


class CreateEnderecoView():
    @csrf_protect
    @api_view(['POST'])
    @authentication_classes([TokenAuthentication])
    def create(request, format=None):
        serializer = EnderecosSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        raise ValidationError(detail="Não foi possível criar endereço, verifique os dados informados \
                e tente novamente.")


class ProfileEnderecoView():
    @api_view(['GET'])
    @authentication_classes([TokenAuthentication])
    def profile(request, format=None):
        endereco = Enderecos.objects.get(owner_id=request.user.pk)
        if endereco is not None :
            serializer = EnderecosSerializer(endereco)
            return Response(serializer.data, status=status.HTTP_200_OK)
        raise NotFound(detail="Não foi possível exibir seu endereço.")


class UpdateEnderecoView():
    @csrf_protect
    @api_view(['PUT', 'POST'])
    @authentication_classes([TokenAuthentication])
    def update(request, pk, format=None):
        endereco = get_endereco(pk)
        serializer = EnderecosSerializer(endereco, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        raise ValidationError(detail="Não foi possível atualizar seu endereço, \
                verifique os dados informados e tente novamente.")