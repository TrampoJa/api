from django.http import *
from django.views.decorators.csrf import csrf_protect

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.authentication import TokenAuthentication

from .serializers import InteressesSerializer
from .models import Interesses
from .permissions import IsFreelancerOrReadOnly
from .tasks import task_send_interesse_message

from ofertas.views import get_oferta


def get_interesse(pk):
    try:
        return Interesses.objects.get(pk=pk)
    except Interesses.DoesNotExist:
        raise Http404


class CreateInteresseView():
    @csrf_protect
    @api_view(['POST'])
    @authentication_classes([TokenAuthentication])
    def create(request, format=None):
        if IsFreelancerOrReadOnly.has_object_permission(request):
            oferta = get_oferta(request.data['id'])
            if Interesses.objects.filter(oferta=oferta, owner=request.user):
                return Response(status=400)
            try:
                i = Interesses.objects.create(oferta=oferta, owner=request.user)
                oferta.edit = False
                oferta.save()
                serializer = InteressesSerializer(i)
                task_send_interesse_message.delay(
                    serializer.data['estabelecimento_email'],
                    serializer.data['freelancer_nome'] + ' ' + serializer.data['freelancer_sobrenome'],
                    serializer.data['oferta_nome']
                )
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception:
                return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=403)


class ListToFreelancerInteresseView():
    @api_view(['GET'])
    @authentication_classes([TokenAuthentication])
    def listToFreelancer(request, format=None):
        interesses = Interesses.objects.filter(owner_id=request.user.pk)
        if interesses is not None:
            serializer = InteressesSerializer(interesses, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ListToEstabelecimentoInteresseView():
    @api_view(['GET'])
    @authentication_classes([TokenAuthentication])
    def listToEstabelecimento(request, format=None):
        interesses = Interesses.objects.filter(oferta__owner_id=request.user.pk)
        if interesses is not None:
            serializer = InteressesSerializer(interesses, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
