from django.http import *
from django.views.decorators.csrf import csrf_protect

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import NotFound, ValidationError, PermissionDenied

from .serializers import PlanosSerializer
from .permissions import IsEstabelecimentoOrReadOnly
from .models import Planos

from estabelecimentos.models import Estabelecimentos
from estabelecimentos.serializers import EstabelecimentosSerializer


class setPlanoEstabelecimento():
    @csrf_protect
    @api_view(['POST'])
    @authentication_classes([TokenAuthentication])
    def set_plano(request, format=None):
        estabelecimento = Estabelecimentos.manager.get_estabelecimento(request.data['estabelecimento']) 
        plano = Planos.manager.get_plano(request.data['plano'])

        if IsEstabelecimentoOrReadOnly.has_object_permission(request):
            # Aqui será a chamada do gateway de pagamento
            # Se der tudo certo continua e seta o plano e o historico para o estabelecimento         
            try:
                estabelecimento = Planos.manager.set_plano(estabelecimento, plano)
                estabelecimento = EstabelecimentosSerializer(estabelecimento)
                return Response(estabelecimento)
            except Exception:
                raise ValidationError("Não foi possível definir seu plano.")

        raise PermissionDenied(detail=["Você não tem permissão para isso."])   


class ListPlanosView():    
    @api_view(['GET'])
    @authentication_classes([TokenAuthentication])
    def liste(request, format=None):
        planos = Planos.manager.all()

        if planos is not None :
            planos = PlanosSerializer(planos, many=True)
            return Response(planos.data, status=status.HTTP_200_OK)

        raise NotFound(detail="Não foi possível exibir os planos.")