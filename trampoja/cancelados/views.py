import datetime
from datetime import timedelta

from django.http import *
from django.views.decorators.csrf import csrf_protect

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.authentication import TokenAuthentication

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
        raise Http404


class CreateCanceladoView():    
    @csrf_protect
    @api_view(['POST'])
    @authentication_classes([TokenAuthentication])
    def create(request, format=None):
        oferta = get_oferta(request.data['oferta'])
        freelancer = get_freelancer(request.data['freelancer'])
        confirmado = get_confirmado(request.data['confirmado'])
        hora_limite = datetime.datetime.now() + timedelta(hours=6)
        
        if IsOwnerOrReadOnly.has_object_permission(request):
            autor = 'F' if request.user.last_name == "Freelancer" else 'E'
            if oferta.date_inicial == datetime.date.today():
                if hora_limite.time() > oferta.time:
                    oferta.closed = True
                    oferta.save()
                    return Response(
                        {"error": "Não foi possível cancelar oferta por \
                            que passou da hora limite."},
                        status=404)
            if oferta.date_inicial < datetime.date.today():
                oferta.closed = True
                oferta.save()
                return Response(
                    {"error": "Não foi possível cancelar oferta."},
                    status=404)
            try:
                c = Cancelados.objects.create(oferta=oferta, owner=freelancer.owner, autor=autor,
                    justificativa=request.data['justificativa'])   
                oferta.status = True
                oferta.canceled = True
                oferta.save()
                confirmado.delete()
                serializer = CanceladosSerializer(c)
                if request.user.last_name == 'Freelancer':
                    task_send_cancelados_message.delay(
                        serializer.data['estabelecimento_email'],
                        serializer.data['freelancer_nome'],
                        serializer.data['oferta_nome'],
                    )
                if request.user.last_name == 'Estabelecimento':
                    task_send_cancelados_message.delay(
                        serializer.data['freelancer_email'],
                        serializer.data['estabelecimento'],
                        serializer.data['oferta_nome'],
                    )
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception:
               return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=403)


class ListToFreelancerCanceladosView():
    @api_view(['GET'])
    @authentication_classes([TokenAuthentication])
    def listToFreelancer(request, format=None):
        cancelados = Cancelados.objects.filter(owner_id=request.user.pk)
        if cancelados is not None:
            serializer = CanceladosSerializer(cancelados, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ListToEstabelecimentoCanceladosView():
    @api_view(['GET'])
    @authentication_classes([TokenAuthentication])
    def listToEstabelecimento(request, format=None):
        cancelados = Cancelados.objects.filter(oferta__owner_id=request.user.pk)
        if cancelados is not None:
            serializer = CanceladosSerializer(cancelados, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)