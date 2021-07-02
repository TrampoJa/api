from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required

from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import ValidationError, PermissionDenied

from .models import Estabelecimentos
from .permissions import IsOwnerOrReadOnly
from .serializers import EstabelecimentosSerializer

from utils.validator import Validator
from utils.formater import Formater


class UploadImageView():
    @csrf_protect
    @api_view(['POST'])
    @authentication_classes([TokenAuthentication])
    @login_required()
    def upload(request, pk, format=None):
        Validator(request.data)
        estabelecimento = Estabelecimentos.manager.get_estabelecimento(pk)

        if IsOwnerOrReadOnly.has_object_permission(request, estabelecimento):
            try:
                image = Formater.formaterImageName(
                    request.data['logo'], 'logo')
                
                Estabelecimentos.manager.set_logo(estabelecimento, image)
                estabelecimento = EstabelecimentosSerializer(estabelecimento)
                return Response(
                    {"logo": estabelecimento.data['logo']}, status=200)
            except Exception:
                raise ValidationError(
                    detail="Não foi possível fazer o upload da sua logo.")

        raise PermissionDenied(detail=["Você não tem permissão para isso."])
