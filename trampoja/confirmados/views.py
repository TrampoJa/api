import datetime

from django.http import *
from django.views.decorators.csrf import csrf_protect

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import ValidationError, NotFound, PermissionDenied

from .serializers import ConfirmadosSerializer
from .models import Confirmados
from .permissions import IsEstabelecimentoOrReadOnly
from .tasks import task_send_confirmados_message

from ofertas.views import get_oferta

from freelancers.views import get_freelancer


def get_confirmado(pk):
    try:
        return Confirmados.objects.get(pk=pk)
    except Confirmados.DoesNotExist:
        raise NotFound(detail=["Confirmado não encontrado."])


class CreateConfirmadoView():    
    @csrf_protect
    @api_view(['POST'])
    @authentication_classes([TokenAuthentication])
    def create(request, format=None):
        if IsEstabelecimentoOrReadOnly.has_object_permission(request):
            oferta = get_oferta(request.data['oferta'])
            freelancer = get_freelancer(request.data['freelancer'])
            if oferta.status == False:
                raise ValidationError(detail="Este trampo já está confirmado.")
            if oferta.date_inicial < datetime.date.today():
                raise ValidationError(detail="Este trampo já aconteceu ou passou da data.")
            try:
                c = Confirmados.objects.create(oferta=oferta, owner=freelancer.owner)
                oferta.status = False
                oferta.save()
                serializer = ConfirmadosSerializer(c)
                task_send_confirmados_message.delay(
                    serializer.data['freelancer_email'],
                    serializer.data['estabelecimento'],
                    serializer.data['oferta_nome']
                )
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception:
                raise ValidationError(detail="Não foi possível confirmar este trampo.")
        raise PermissionDenied(detail=["Você não tem permissão para isso."])


class ListToFreelancerConfirmadoView():
    @api_view(['GET'])
    @authentication_classes([TokenAuthentication])
    def listToFreelancer(request, format=None):
        confirmados = Confirmados.objects.filter(owner_id=request.user.pk)
        if confirmados is not None:
            serializer = ConfirmadosSerializer(confirmados, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        raise NotFound(detail=["Não foi possível exibir os trampos confirmados."])


class ListToEstabelecimentoConfirmadoView():
    @api_view(['GET'])
    @authentication_classes([TokenAuthentication])
    def listToEstabelecimento(request, format=None):
        confirmados = Confirmados.objects.filter(oferta__owner_id=request.user.pk)
        if confirmados is not None:
            serializer = ConfirmadosSerializer(confirmados, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        raise NotFound(detail=["Não foi possível exibir os trampos confirmados."])
