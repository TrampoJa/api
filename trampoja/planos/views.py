from django.http import *
from django.views.decorators.csrf import csrf_protect

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import NotFound

from .serializers import PlanosSerializer
from .models import Planos


def get_plano(pk):
    try:
        return Planos.objects.get(pk=pk)
    except Planos.DoesNotExist:
        raise NotFound(detail="Plano não encontrado.")


class setPlanoEstabelecimento():
    @csrf_protect
    @api_view(['POST'])
    @authentication_classes([TokenAuthentication])
    def create(request, format=None):
        pass


class ListPlanosView():    
    @api_view(['GET'])
    @authentication_classes([TokenAuthentication])
    def liste(request, format=None):
        planos = Planos.objects.all()
        if planos is not None :
            serializer = PlanosSerializer(planos, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        raise NotFound(detail="Não foi possível exibir os planos.")


class ProfilePlanosView():
    @api_view(['GET'])
    @authentication_classes([TokenAuthentication])
    def profile(request, format=None):
        planos = Planos.objects.filter(owner_id=request.user.pk)
        if planos is not None :
            serializer = PlanosSerializer(planos, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        raise NotFound(detail="Não foi possível exibir seu plano.")