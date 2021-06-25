from random import randint

from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError, NotFound, NotAuthenticated

from .serializers import UserSerializer
from .tasks import task_send_welcome_message, task_send_recovery_message

from utils.validator import Validator
from utils.formater import Formater


def get_user(pk):
    try:
        return User.objects.get(pk=pk)
    except User.DoesNotExist:
        raise NotFound(detail=["Usuário não encontrado."])


class CreateUserView():
    @csrf_protect
    @api_view(['POST'])
    def create(request, format=None):
        Validator(request.data)
        
        try:
            user = User.objects.get(email=request.data['email'])          
            return Response(["Email já cadastrado"], status=400)
        except Exception:
            ...
        
        try:
            user = User.objects.create_user(
                request.data['username'],
                request.data['email'],
                request.data['password'],
            )
            formater = Formater(
                [request.data['first_name'], request.data['last_name']])
            user.first_name = formater[0] + ' ' + formater[1]
            user.save()
            Token.objects.create(user=user)
            serializer = UserSerializer(user)
            task_send_welcome_message.delay(user.email, user.first_name)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception:
            raise ValidationError(detail=
                    'Não foi possível realizar cadastro, '
                    'verfique os dados informados e tente novamente.'
                )


class ProfileUserView():
    @api_view(['GET'])
    @authentication_classes([TokenAuthentication])
    @login_required()
    def profile(request, format=None):
        user = get_user(request.user.pk)
        if user is not None:
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        raise NotFound(detail=["Não foi possível exibir seus dados."])


class DetailUserView():
    @api_view(['GET'])
    @authentication_classes([TokenAuthentication])
    @login_required()
    def detail(request, pk, format=None):
        user = get_user(pk)
        if user is not None:
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        raise NotFound(
            detail="Não foi possível exibir os detalhes do usuário.")


class ChangeEmailView():
    @csrf_protect
    @api_view(['PUT', 'POST'])
    @authentication_classes([TokenAuthentication])
    @login_required()
    def setEmail(request, format=None):
        Validator(request.data)
        
        try:
            user = User.objects.get(email=request.data['email'])          
            return Response(["Email já cadastrado"], status=400)
        except Exception:
            ...

        try:
            user = request.user
            user.email = request.data['email']
            user.username = request.data['email']
            user.save()
            return Response(user.username, status=status.HTTP_200_OK)
        except Exception:
            raise ValidationError(detail="Não foi possível alterar seu email.")


class ChangePasswordView():
    @csrf_protect
    @api_view(['PUT', 'POST'])
    @authentication_classes([TokenAuthentication])
    @login_required()
    def setPassword(request, format=None):
        Validator(request.data)
        try:
            user = request.user
            user.set_password(request.data['password'])
            user.save()
            return Response({'success': 'success'}, status=status.HTTP_200_OK)
        except Exception:
            raise ValidationError(detail="Não foi possível alterar sua senha.")


class RecoveryPasswordView():
    @csrf_protect
    @api_view(['POST'])
    def recovery(request, format=None):
        try:
            user = User.objects.get(username=request.data['email'])
            new_password = str(randint(100000, 999999))
            user.set_password(new_password)
            task_send_recovery_message.delay(
                user.email, user.first_name, new_password)
            user.save()
            return Response({"success": "success"}, status=200)
        except Exception:
            raise NotFound(detail=["Este email não está cadastrado."])


class Login():
    @csrf_protect
    @api_view(['POST'])
    def login(request, format=None):
        try:
            username = request.data['username']
            password = request.data['password']
            user = authenticate(username=username, password=password)
            if user.is_authenticated:
                login(request, user)
                serializer = UserSerializer(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                raise NotAuthenticated(detail="Não foi possível fazer login.")
        except Exception:
            raise ValidationError(detail=["Email ou senha inválidos."])
