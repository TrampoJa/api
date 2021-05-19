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

from estabelecimentos.views import get_estabelecimento
from estabelecimentos.serializers import EstabelecimentosSerializer

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
        estabelecimento = get_estabelecimento(request.data['estabelecimento'])
        plano = get_plano(request.data['plano'])
        if IsEstabelecimentoOrReadOnly.has_object_permission(request):

            # Aqui será a chamada do gateway de pagamento
            # O parametro estabelecimento será para buscar os dados da compra, cartão etc
            # O parametro plano será para buscar o valor a ser cobrado
            # Se der tudo certo continua e seta o plano para o estabelecimento
            
            try:
                estabelecimento.plano_contratado = plano
                estabelecimento.ofertas_para_publicar = plano.quantidade
                estabelecimento.save()
                e = EstabelecimentosSerializer(e)
                return Response(e)
            except Exception:
                raise ValidationError("Não foi possível definir seu plano.")
        raise PermissionDenied(detail=["Você não tem permissão para isso."])   


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