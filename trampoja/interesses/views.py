from django.views.decorators.csrf import csrf_protect

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import ValidationError, NotFound, PermissionDenied

from .serializers import InteressesSerializer
from .models import Interesses
from .permissions import IsFreelancerOrReadOnly
from .tasks import task_send_interesse_message

from ofertas.views import get_oferta


def get_interesse(pk):
    try:
        return Interesses.objects.get(pk=pk)
    except Interesses.DoesNotExist:
        raise NotFound(detail=["Interesse não encontrado."])


class CreateInteresseView():
    @csrf_protect
    @api_view(['POST'])
    @authentication_classes([TokenAuthentication])
    def create(request, format=None):
        if IsFreelancerOrReadOnly.has_object_permission(request):
            oferta = get_oferta(request.data['id'])
            if Interesses.objects.filter(oferta=oferta, owner=request.user):
                raise ValidationError(
                    detail="Você já demonstrou interesse nesse trampo.")
            try:
                i = Interesses.objects.create(
                    oferta=oferta, owner=request.user)
                oferta.edit = False
                oferta.save()
                serializer = InteressesSerializer(i)
                task_send_interesse_message.delay(
                    serializer.data['estabelecimento_email'],
                    serializer.data['freelancer_nome'] + ' ' +
                    serializer.data['freelancer_sobrenome'],
                    serializer.data['oferta_nome']
                )
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception:
                raise ValidationError(
                    detail="Não foi possível demonstrar interesse neste trampo.")
        raise PermissionDenied(detail=["Você não tem permissão para isso."])


class ListToFreelancerInteresseView():
    @api_view(['GET'])
    @authentication_classes([TokenAuthentication])
    def listToFreelancer(request, format=None):
        interesses = Interesses.objects.filter(owner_id=request.user.pk)
        if interesses is not None:
            serializer = InteressesSerializer(interesses, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        raise NotFound(detail=["Não foi possível exibir seus interesses."])


class ListToEstabelecimentoInteresseView():
    @api_view(['GET'])
    @authentication_classes([TokenAuthentication])
    def listToEstabelecimento(request, format=None):
        interesses = Interesses.objects.filter(
            oferta__owner_id=request.user.pk)
        if interesses is not None:
            serializer = InteressesSerializer(interesses, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        raise NotFound(detail=["Não foi possível exibir seus interesses."])
