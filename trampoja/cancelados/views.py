import datetime
from datetime import timedelta

from django.http import *
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import ValidationError, NotFound, PermissionDenied

from .serializers import CanceladosSerializer
from .models import Cancelados
from .permissions import IsOwnerOrReadOnly
from .tasks import task_send_cancelados_message

from ofertas.views import get_oferta

from freelancers.views import get_freelancer

from confirmados.views import get_confirmado


def get_cancelado(pk):
    try:
        return Cancelados.objects.get(pk=pk)
    except Cancelados.DoesNotExist:
        raise NotFound(deatil="Cancelado não encontrado.")


class CreateCanceladoView():
    @csrf_protect
    @api_view(['POST'])
    @authentication_classes([TokenAuthentication])
    @login_required()
    def create(request, format=None):
        oferta = get_oferta(request.data['oferta'])
        freelancer = get_freelancer(request.data['freelancer'])
        confirmado = get_confirmado(request.data['confirmado'])
        hora_limite = datetime.datetime.now() + timedelta(hours=6)

        if IsOwnerOrReadOnly.has_object_permission(request):
            autor = 'F' if request.user.groups.get().name == "Freelancer" else 'E'
            if oferta.date_inicial == datetime.date.today():
                if hora_limite.time() > oferta.time:
                    oferta.closed = True
                    oferta.save()
                    raise ValidationError(detail=
                            'Não foi possível cancelar trampo, '
                            'só é possível cancelar com 6 horas de antecedência.'
                        )
            if oferta.date_inicial < datetime.date.today():
                oferta.closed = True
                oferta.save()
                raise ValidationError(detail=
                        'Não foi possível cancelar. '
                        'Esse trampo já aconteceu.'
                    )
            try:
                c = Cancelados.objects.create(oferta=oferta, owner=freelancer.owner, autor=autor,
                                              justificativa=request.data['justificativa'])
                oferta.status = True
                oferta.canceled = True
                oferta.save()
                confirmado.delete()
                serializer = CanceladosSerializer(c)
                if request.user.groups.get().name == 'Freelancer':
                    task_send_cancelados_message.delay(
                        serializer.data['estabelecimento_email'],
                        serializer.data['freelancer_nome'],
                        serializer.data['oferta_nome'],
                    )
                if request.user.groups.get().name == 'Estabelecimento':
                    task_send_cancelados_message.delay(
                        serializer.data['freelancer_email'],
                        serializer.data['estabelecimento'],
                        serializer.data['oferta_nome'],
                    )
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception:
                raise ValidationError(
                    detail="Não foi possível cancelar este trampo.")
        raise PermissionDenied(detail=["Você não tem permissão para isso."])


class ListToFreelancerCanceladosView():
    @api_view(['GET'])
    @authentication_classes([TokenAuthentication])
    @login_required()
    def listToFreelancer(request, format=None):
        cancelados = Cancelados.objects.filter(owner_id=request.user.pk)
        if cancelados is not None:
            serializer = CanceladosSerializer(cancelados, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        raise NotFound(
            detail=["Não foi possível exibir os trampos cancelados."])


class ListToEstabelecimentoCanceladosView():
    @api_view(['GET'])
    @authentication_classes([TokenAuthentication])
    @login_required()
    def listToEstabelecimento(request, format=None):
        cancelados = Cancelados.objects.filter(
            oferta__owner_id=request.user.pk)
        if cancelados is not None:
            serializer = CanceladosSerializer(cancelados, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        raise NotFound(
            detail=["Não foi possível exibir os trampos cancelados."])
