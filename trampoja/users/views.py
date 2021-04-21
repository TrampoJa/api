from random import randint

from django.http import *
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics
from rest_framework.authtoken.models import Token

from .serializers import UserSerializer
from .utils import Utils
from .tasks import task_send_welcome_message, task_send_recovery_message


def get_user(pk):
    try:
        return User.objects.get(pk=pk)
    except User.DoesNotExist:
        raise Http404


class CreateUserView():      
    @csrf_protect
    @api_view(['POST'])
    def create(request, format=None):
        Utils().validator(
            email = request.data['email'], 
            password = request.data['password']
        )
        try:
            user = User.objects.create_user(
                request.data['username'],
                request.data['email'],
                request.data['password'],
            )
            user.first_name = request.data['first_name'] + ' ' + request.data['last_name']
            user.save()
            token = Token.objects.create(user=user)
            serializer = UserSerializer(user)
            task_send_welcome_message.delay(user.email, user.first_name)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ProfileUserView(): 
    @api_view(['GET'])
    @authentication_classes([TokenAuthentication])
    def profile(request, format=None):
        user = get_user(request.user.pk)
        if user is not None :
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class DetailUserView(): 
    @api_view(['GET'])
    @authentication_classes([TokenAuthentication])
    def detail(request, pk, format=None):
        user = get_user(pk)
        if user is not None :
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ChangeEmailView(): 
    @csrf_protect
    @api_view(['PUT', 'POST'])
    @authentication_classes([TokenAuthentication])
    def setEmail(request, format=None):
        Utils().email_validator(email=request.data['email'])    
        try:
            user = request.user
            user.email = request.data['email']
            user.username = request.data['email']
            user.save()
            return Response(user.username, status=status.HTTP_200_OK)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView():
    @csrf_protect
    @api_view(['PUT', 'POST'])
    @authentication_classes([TokenAuthentication])
    def setPassword(request, format=None):
        Utils().password_validator(password=request.data['password'])
        try:
            user = request.user
            user.set_password(request.data['password'])
            user.save()
            return Response({'success': 'success'}, status=status.HTTP_200_OK)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class RecoveryPasswordView():
    @csrf_protect
    @api_view(['POST'])
    @authentication_classes([TokenAuthentication])
    def recovery(request, format=None):
        try:
            user = User.objects.get(username=request.data['email'])
            new_password = str(randint(100000, 999999))
            user.set_password(new_password)
            task_send_recovery_message.delay(user.email, user.first_name, new_password)
            user.save()
            return Response({"success": "success"}, status=200)
        except Exception:
            return Response({"error": "Este email não está cadastrado."}, status=404)


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
            else :
                return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response(status=401)