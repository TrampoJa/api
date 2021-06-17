from django.views.decorators.csrf import csrf_protect

from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import ValidationError, PermissionDenied

from .views import get_freelancer
from .permissions import IsOwnerOrReadOnly
from .serializers import FreeLancersSerializer, DocumentosSerializer
from .models import FreeLancers, Documentos
from utils.validator import Validator


class UploadImageView():
    @csrf_protect
    @api_view(['POST'])
    @authentication_classes([TokenAuthentication])
    def upload(request, pk, format=None):
        Validator(request.data)
        freelancer = get_freelancer(pk)
        if IsOwnerOrReadOnly.has_object_permission(request, freelancer):
            try:
                freelancer.foto = request.data['foto']
                freelancer.save()
                freelancer = FreeLancersSerializer(freelancer)
                return Response({"foto": freelancer.data['foto']}, status=200)
            except Exception:
                raise ValidationError(
                    detail="Não foi possível fazer o upload da sua foto.")
        raise PermissionDenied(detail=["Você não tem permissão para isso."])


class UploadImageDocsView():
    @csrf_protect
    @api_view(['POST'])
    @authentication_classes([TokenAuthentication])
    def upload(request, step, format=None):
        Validator(request.data)
        freelancer = FreeLancers.objects.get(owner=request.user)

        try:
            documento = Documentos.objects.get(freelancer=freelancer)
        except Documentos.DoesNotExist:
            documento = Documentos.objects.create(freelancer=freelancer)

        try:
            if step == 0:
                documento.frente = request.data['foto']
                field = 'frente'

            elif step == 1:
                documento.verso = request.data['foto']
                field = 'verso'

            elif step == 2:
                documento.selfie = request.data['foto']
                field = 'selfie'

            else:
                raise ValidationError(
                    detail="Não entendi o que pretende fazer.")
            documento.save()
            documento = DocumentosSerializer(documento)
            return Response({"foto": documento.data[field]}, status=200)

        except Exception:
            raise ValidationError(
                detail="Não foi possível fazer o upload da sua foto.")
