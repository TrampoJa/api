from django.views.decorators.csrf import csrf_protect

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import ValidationError, NotFound, PermissionDenied

from .serializers import FreeLancersSerializer
from .models import FreeLancers
from .permissions import IsOwnerOrReadOnly

from users.views import get_user
from users.serializers import UserSerializer

from confirmados.models import Confirmados
from confirmados.serializers import ConfirmadosSerializer

from utils.validator import Validator


def get_freelancer(pk):
    try:
        return FreeLancers.objects.get(pk=pk)
    except FreeLancers.DoesNotExist:
        raise NotFound(detail=["Freelancer não encontrado."])


class CreateFreeLancerView():
    @csrf_protect
    @api_view(['POST'])
    @authentication_classes([TokenAuthentication])
    def create(request, format=None):
        user = get_user(request.user.id)
        serializer = FreeLancersSerializer(data=request.data)
        if serializer.is_valid():
            Validator(serializer.validated_data)
            serializer.save(owner=request.user)
            user.last_name = "Freelancer"
            user.save()
            userSerializer = UserSerializer(user)
            return Response([serializer.data, userSerializer.data],
                            status=status.HTTP_201_CREATED)
        raise ValidationError(detail="Não foi possível finalizar seu cadastro, \
                verifique os dados informados e tente novamente")


class ListFreeLancerView():
    @api_view(['GET'])
    @authentication_classes([TokenAuthentication])
    def liste(request, format=None):
        freelancers = FreeLancers.objects.all()
        if freelancers is not None:
            serializer = FreeLancersSerializer(freelancers, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        raise NotFound(detail=["Não foi possível exibir os freelancers."])


class ProfileFreeLancerView():
    @api_view(['GET'])
    @authentication_classes([TokenAuthentication])
    def profile(request, format=None):
        freelancer = FreeLancers.objects.get(owner_id=request.user.pk)
        if freelancer is not None:
            serializer = FreeLancersSerializer(freelancer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        raise NotFound(detail=["Não foi possível exibir seus dados."])


class DetailFreeLancerView():
    @api_view(['GET'])
    @authentication_classes([TokenAuthentication])
    def detail(request, pk, format=None):
        freelancer = get_freelancer(pk)
        if IsOwnerOrReadOnly.has_object_permission(request, freelancer):
            if freelancer is not None:
                serializer = FreeLancersSerializer(freelancer)
                return Response(serializer.data, status=status.HTTP_200_OK)
            raise NotFound(detail=["Não foi possível exibir seus dados."])
        raise PermissionDenied(detail=["Você não tem permissão para isso."])


class UpdateFreeLancerView():
    @csrf_protect
    @api_view(['PUT', 'POST'])
    @authentication_classes([TokenAuthentication])
    def update(request, pk, format=None):
        freelancer = get_freelancer(pk)
        if IsOwnerOrReadOnly.has_object_permission(request, freelancer):
            serializer = FreeLancersSerializer(freelancer, data=request.data)
            if serializer.is_valid():
                Validator(serializer.validated_data)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            raise ValidationError(detail="Não foi possível atualizar seus dados, \
                    verifique os dados informados e tente novamente.")
        raise PermissionDenied(detail=["Você não tem permissão para isso."])


class DeleteFreeLancerView():
    @api_view(['DELETE'])
    @authentication_classes([TokenAuthentication])
    def delete(request, pk, format=None):
        freelancer = get_freelancer(pk)
        if IsOwnerOrReadOnly.has_object_permission(request, freelancer):
            try:
                freelancer.delete()
                return Response(status=status.HTTP_200_OK)
            except Exception:
                raise ValidationError(detail="Algo deu errado.")
        raise PermissionDenied(detail=["Você não tem permissão para isso."])


class CountOfertasConfirmadasFreelancerView():
    @api_view(['GET'])
    @authentication_classes([TokenAuthentication])
    def count(request, format=None):
        try:
            freelancer = FreeLancers.objects.get(owner=request.user)
            count = Confirmados.objects.filter(
                owner=freelancer.owner, oferta_id__closed=True).count()
            return Response(count)
        except Exception:
            raise NotFound(
                detail="Não foi possíbel exibir o número de trampos")


class HistoricoFreelancerView():
    @api_view(['GET'])
    @authentication_classes([TokenAuthentication])
    def historico(request, pk, format=None):
        try:
            historico = []

            freelancer = FreeLancers.objects.get(owner=pk)
            confirmados = Confirmados.objects.filter(
                owner=freelancer.owner, oferta_id__closed=True)
            serializer = ConfirmadosSerializer(confirmados, many=True)

            for data in serializer.data:
                aux = {
                    'estabelecimento': data['estabelecimento'],
                    'data': data['oferta_data'],
                    'vaga': data['oferta_nome']
                }
                historico.append(aux)

            return Response(historico)
        except Exception:
            raise ValidationError(
                detail='Não foi possível exibir o histórico.')
