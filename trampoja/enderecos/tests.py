from django.test import TestCase
from users.views import User
from enderecos.models import Enderecos
from enderecos.serializers import EnderecosSerializer
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.http import *


class TestEnderecos(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.writer = User.objects.create_user(
            'test_user',
            'test@example.com', 
            'password1'
        )
        self.token = Token.objects.create(user=self.writer)

        self.writer2 = User.objects.create_user(
            'test2_user',
            'test2@example.com', 
            'password1'
        )
        self.token2 = Token.objects.create(user=self.writer2)

        self.endereco = Enderecos(
            estado = 'Santa Catarina',
            cidade = 'Chapeco',
            bairro = 'Bairro Teste',
            rua = 'Rua teste',
            numero = '10',
            complemento = '',
            logradouro = '',
            owner  = self.writer2
        )
        self.endereco.save()


class TestEnderecosCreateView(TestEnderecos):    
    def test_create_endereco_post_sucess(self):
        data = {
            'estado': 'Santa Catarina',
            'cidade': 'Chapeco',
            'bairro': 'Bairro Teste',
            'rua': 'Rua teste',
            'numero': '10',
            'complemento': '',
            'logradouro': '',
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)    
        response = self.client.post("/endereco/create", data)
        self.assertEqual(response.status_code, 201)
    
    """
    Como nenhum campo é obrigatório no banco,
    esta representação genérica de erro não é válida

    def test_create_endereco_post_error(self):
        data = {
            'estado': '',
            'cidade': '',
            'bairro': '',
            'rua': '',
            'numero': '',
            'complemento': '',
            'logradouro': '',
        }    
        response = self.client.post("/create-endereco/", data)
        self.assertEqual(response.status_code, 400)
    """


class TestEnderecosProfileView(TestEnderecos): 
    def test_profile_endereco_error(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + '')
        response = self.client.get("/endereco/profile")
        self.assertEqual(response.status_code, 401)
 
    def test_profile_endereco_sucess(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token2.key)
        if self.client.login(username='test2_user', password='password1') :
            response = self.client.get("/endereco/profile")
        self.assertEqual(response.status_code, 200)


class TestEnderecoUpdateView(TestEnderecos): 
    def test_update_endereco_post_error(self):
        data = {
            'estado': '',
            'cidade': '',
            'bairro': '',
            'rua': '',
            'numero': '',
            'complemento': '',
            'logradouro': '',
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)    
        response = self.client.put("/endereco/update/0", data)
        self.assertEqual(response.status_code, 404)

    def test_update_endereco_post_sucess(self):
        data = {
            'estado': 'Santa Catarina',
            'cidade': 'Slo',
            'bairro': 'Bairro Teste',
            'rua': 'Rua teste',
            'numero': '10',
            'complemento': '',
            'logradouro': '',
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)    
        response = self.client.post("/endereco/update/1", data)
        self.assertEqual(response.status_code, 200)