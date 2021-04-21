from django.http import *
from django.views.decorators.csrf import csrf_protect

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.authentication import TokenAuthentication

from .serializers import EnderecosSerializer
from .models import Enderecos


def get_endereco(pk):
    try:
        return Enderecos.objects.get(pk=pk)
    except Enderecos.DoesNotExist:
        raise Http404


class CreateEnderecoView():
    @csrf_protect
    @api_view(['POST'])
    @authentication_classes([TokenAuthentication])
    def create(request, format=None):
        serializer = EnderecosSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)


class ProfileEnderecoView():
    @api_view(['GET'])
    @authentication_classes([TokenAuthentication])
    def profile(request, format=None):
        endereco = Enderecos.objects.get(owner_id=request.user.pk)
        if endereco is not None :
            serializer = EnderecosSerializer(endereco)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


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
        return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)