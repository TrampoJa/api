import datetime

from django.http import *
from django.views.decorators.csrf import csrf_protect

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.authentication import TokenAuthentication

from .serializers import OfertasSerializer
from .utils import Utils
from .models import Ofertas
from .permissions import IsOwnerOrReadOnly
from .tasks import task_send_nova_oferta_message


def get_oferta(pk):
    try:
        return Ofertas.objects.get(pk=pk)
    except Ofertas.DoesNotExist:
        raise Http404


class CreateOfertaView():
    @csrf_protect
    @api_view(['POST'])
    @authentication_classes([TokenAuthentication])
    def create(request, format=None):
        freelancers = int(request.data['freelancers'])
        response = []
        if freelancers > 1:
            for i in range(freelancers):
                serializer = OfertasSerializer(data=request.data)
                if serializer.is_valid():
                    Utils.validator(serializer.validated_data)
                    serializer.save(owner=request.user)
                    response.append(serializer.data)
                else:
                    return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)
            task_send_nova_oferta_message.delay()
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            serializer = OfertasSerializer(data=request.data)
            if serializer.is_valid():
                Utils.validator(serializer.validated_data)
                serializer.save(owner=request.user)
                task_send_nova_oferta_message.delay()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)


class ListOfertaView():    
    @api_view(['GET'])
    @authentication_classes([TokenAuthentication])
    def liste(request, format=None):
        ofertas = Ofertas.objects.filter(date_inicial__gte=datetime.date.today())
        if ofertas is not None :
            serializer = OfertasSerializer(ofertas, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ProfileOfertaView():
    @api_view(['GET'])
    @authentication_classes([TokenAuthentication])
    def profile(request, format=None):
        ofertas = Ofertas.objects.filter(owner_id=request.user.pk).exclude(status=False)
        if ofertas is not None :
            serializer = OfertasSerializer(ofertas, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class DetailOfertaView():
    @api_view(['GET'])
    @authentication_classes([TokenAuthentication])
    def detail(request, pk, format=None):
        oferta = get_oferta(pk)
        if IsOwnerOrReadOnly.has_object_permission(request, oferta):
            if oferta is not None :
                serializer = OfertasSerializer(oferta)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=403)


class UpdateOfertaView():
    @csrf_protect
    @api_view(['PUT', 'POST'])
    @authentication_classes([TokenAuthentication])
    def update(request, pk, format=None):
        oferta = get_oferta(pk)
        if oferta.edit == False:
            return Response(status=400)
        if IsOwnerOrReadOnly.has_object_permission(request, oferta):
            serializer = OfertasSerializer(oferta, data=request.data)
            if serializer.is_valid():
                Utils.validator(serializer.validated_data)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=403)
        

class DeleteOfertaView():
    @api_view(['DELETE'])
    @authentication_classes([TokenAuthentication])
    def delete(request, pk, format=None):
        oferta = get_oferta(pk)
        if IsOwnerOrReadOnly.has_object_permission(request, oferta):
            try:
                oferta.delete()
                return Response(status=status.HTTP_200_OK)
            except Exception:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=403)