from django.http import *
from django.views.decorators.csrf import csrf_protect

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.authentication import TokenAuthentication

from .serializers import FreeLancersSerializer
from .models import FreeLancers
from .utils import Utils
from .permissions import IsOwnerOrReadOnly

from users.views import get_user
from users.serializers import UserSerializer

from confirmados.models import Confirmados
from confirmados.serializers import ConfirmadosSerializer


def get_freelancer(pk):
    try:
        return FreeLancers.objects.get(pk=pk)
    except FreeLancers.DoesNotExist:
        raise Http404


class CreateFreeLancerView():    
    @csrf_protect
    @api_view(['POST'])
    @authentication_classes([TokenAuthentication])
    def create(request, format=None):
        user = get_user(request.user.id)
        serializer = FreeLancersSerializer(data=request.data)
        if serializer.is_valid():
            Utils.validator(serializer.validated_data)
            serializer.save(owner=request.user)
            user.last_name = "Freelancer"
            user.save()
            userSerializer = UserSerializer(user)
            return Response([serializer.data, userSerializer.data], status=status.HTTP_201_CREATED)
        return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)


class ListFreeLancerView():
    @api_view(['GET'])
    @authentication_classes([TokenAuthentication])
    def liste(request, format=None):
        freelancers = FreeLancers.objects.all()
        if freelancers is not None :
            serializer = FreeLancersSerializer(freelancers, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ProfileFreeLancerView():
    @api_view(['GET'])
    @authentication_classes([TokenAuthentication])
    def profile(request, format=None):
        freelancer = FreeLancers.objects.get(owner_id=request.user.pk)
        if freelancer is not None :
            serializer = FreeLancersSerializer(freelancer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class DetailFreeLancerView():
    @api_view(['GET'])
    @authentication_classes([TokenAuthentication])
    def detail(request, pk, format=None):
        freelancer = get_freelancer(pk)
        if IsOwnerOrReadOnly.has_object_permission(request, freelancer):
            if freelancer is not None :
                serializer = FreeLancersSerializer(freelancer)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=403)


class UpdateFreeLancerView():
    @csrf_protect
    @api_view(['PUT', 'POST'])
    @authentication_classes([TokenAuthentication])
    def update(request, pk, format=None):
        freelancer = get_freelancer(pk)
        if IsOwnerOrReadOnly.has_object_permission(request, freelancer):
            serializer = FreeLancersSerializer(freelancer, data=request.data)
            if serializer.is_valid():
                Utils.validator(serializer.validated_data)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=403)


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
                return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=403)


class CountOfertasConfirmadasFreelancerView():
    @api_view(['GET'])
    @authentication_classes([TokenAuthentication])
    def count(request, format=None):
        try:
            freelancer = FreeLancers.objects.get(owner=request.user)
            count = Confirmados.objects.filter(owner=freelancer.owner, oferta_id__closed=True).count()
            return Response(count)
        except Exception:
            return Response({"error": "Não foi possíbel exibir o número de trampos"}, status=status.HTTP_400_BAD_REQUEST)


class HistoricoFreelancerView():
    @api_view(['GET'])
    @authentication_classes([TokenAuthentication])
    def historico(request, pk, format=None):
        try:
            historico = []
                
            freelancer = FreeLancers.objects.get(owner=pk)
            confirmados = Confirmados.objects.filter(owner=freelancer.owner, oferta_id__closed=True)
            serializer = ConfirmadosSerializer(confirmados, many=True)
                
            for data in serializer.data:
                aux = {
                    'estabelecimento': data['estabelecimento'],
                    'vaga': data['oferta_nome']
                }
                historico.append(aux)

            return Response(historico)
        except Exception:
            return Response({"error": "Não foi possível exibir o histórico"}, status=status.HTTP_400_BAD_REQUEST)