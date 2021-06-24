from django.db.models import Avg
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import ValidationError, NotFound

from .serializers import AvaliacoesSerializer
from .models import Avaliacoes

from users.views import get_user

from ofertas.views import get_oferta


def get_avaliacao(pk):
    try:
        return Avaliacoes.objects.get(pk=pk)
    except Avaliacoes.DoesNotExist:
        raise NotFound(detail=["Avalição não encontrada."])


class CreateAvaliacaoView():
    @csrf_protect
    @api_view(['POST'])
    @authentication_classes([TokenAuthentication])
    @login_required()
    def create(request, format=None):
        owner = get_user(request.data['owner'])
        oferta = get_oferta(request.data['oferta'])
        if Avaliacoes.objects.filter(owner=owner, oferta=oferta):
            raise ValidationError(detail="Ops, você já avaliou este trampo!")
        try:
            a = Avaliacoes.objects.create(
                owner=owner, oferta=oferta, nota=request.data['nota'])
            oferta.closed = True
            oferta.save()
            serializer = AvaliacoesSerializer(a)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception:
            raise ValidationError(
                detail="Ops, não foi possível avaliar este trampos!")


class GetSelfAvaliacaoView():
    @api_view(['GET'])
    @authentication_classes([TokenAuthentication])
    @login_required()
    def getSelf(request, format=None):
        try:
            avaliacoes = Avaliacoes.objects.filter(
                owner=request.user.pk).aggregate(Avg('nota'))
            return Response(avaliacoes['nota__avg'], status=status.HTTP_200_OK)
        except Avaliacoes.DoesNotExist:
            raise NotFound(detail=["Avalição não encontrada."])
