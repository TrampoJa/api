from django.http import *
from django.views.decorators.csrf import csrf_protect

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import ValidationError, PermissionDenied

from .views import get_freelancer
from .permissions import IsOwnerOrReadOnly


class UploadImageView():
    @csrf_protect
    @api_view(['POST'])
    @authentication_classes([TokenAuthentication])
    def upload(request, pk, format=None):
        freelancer = get_freelancer(pk)
        if IsOwnerOrReadOnly.has_object_permission(request, freelancer):
            try:
                freelancer.foto = request.data['foto']
                freelancer.save()
                return Response({"message":"sucess"}, status=200)
            except Exception:
                raise ValidationError(detail="Não foi possível fazer o upload da sua foto.")
        raise PermissionDenied(detail=["Você não tem permissão para isso."])