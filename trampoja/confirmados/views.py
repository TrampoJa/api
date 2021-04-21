import datetime

from django.http import *
from django.views.decorators.csrf import csrf_protect

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.authentication import TokenAuthentication

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
        raise Http404


class CreateConfirmadoView():    
    @csrf_protect
    @api_view(['POST'])
    @authentication_classes([TokenAuthentication])
    def create(request, format=None):
        if IsEstabelecimentoOrReadOnly.has_object_permission(request):
            oferta = get_oferta(request.data['oferta'])
            freelancer = get_freelancer(request.data['freelancer'])
            if oferta.status == False:
                return Response(status=400)
            if oferta.date_inicial < datetime.date.today():
                return Response(status=400)
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
                return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=403)


class ListToFreelancerConfirmadoView():
    @api_view(['GET'])
    @authentication_classes([TokenAuthentication])
    def listToFreelancer(request, format=None):
        confirmados = Confirmados.objects.filter(owner_id=request.user.pk)
        if confirmados is not None:
            serializer = ConfirmadosSerializer(confirmados, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ListToEstabelecimentoConfirmadoView():
    @api_view(['GET'])
    @authentication_classes([TokenAuthentication])
    def listToEstabelecimento(request, format=None):
        confirmados = Confirmados.objects.filter(oferta__owner_id=request.user.pk)
        if confirmados is not None:
            serializer = ConfirmadosSerializer(confirmados, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
